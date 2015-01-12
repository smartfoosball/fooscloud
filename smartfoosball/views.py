# coding:utf-8
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.views.generic import View, TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from models import *
from helper import *
from smartfoosball.settings import *
from smartfoosball.models import *
from smartfoosball.utils import get_qrcode
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply
from wechatpy import parse_message, create_reply
from gservice.client import GServiceClient

import json
import urllib
import requests
import logging
logger = logging.getLogger('django')

class Index(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        return super(Index, self).get(request)


class WechatEcho(View):

    def dispatch(self, *args, **kwargs):
        signature = self.request.GET.get('signature', '')
        timestamp = self.request.GET.get('timestamp', '')
        nonce = self.request.GET.get('nonce', '')

        try:
            check_signature(settings.TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            return HttpResponse(status=403)

        return super(WechatEcho, self).dispatch(*args, **kwargs)

    def get(self, request):
        echo_str = request.GET.get('echostr', '')
        return HttpResponse(echo_str)

    def post(self, request):
        msg = parse_message(request.body)
        if msg.type == 'event':
            if msg.event == 'subscribe':
                # 订阅时的事件
                reply = create_reply(u'菜鸟，来一局...', msg)
                return HttpResponse(reply.render())
            elif msg.event in ['scan', 'subscribe_scan']:
                try:
                    fb = FoosBall.objects.get(scene_id=msg.scene_id)
                    gsc = GServiceClient(settings.GW_APPID)
                    resp = gsc.query_device(
                        settings.PRODUCT_KEY, fb.mac).json()
                    did = resp.get('did')
                    if did and did != fb.did:
                        fb.did = did
                        fb.passcode = resp.get('passcode')
                        fb.save()
                        get_gservice_client2(settings.GW_APPID, settings.GW_USER, settings.GW_PWD).bind_device(
                            [(fb.did, fb.passcode)])

                    try:
                        p = Player.objects.get(openid=msg.source)
                    except Player.DoesNotExist:
                        p = Player(openid=msg.source)
                        p.save()
                    finally:
                        p.foosball.add(fb)
                except FoosBall.DoesNotExist:
                    pass
                except Exception:
                    pass
                reply = create_reply(u'菜鸟，来一局...', msg)
                return HttpResponse(reply.render())

        reply = TextReply(content=u'你好，有任何问题请直接回复，我们会尽快处理。', message=msg)
        return HttpResponse(reply.render())


class BaseWeixinView(View):

    def dispatch(self, *args, **kwargs):
        if (not self.request.user.is_authenticated()) or\
           (not hasattr(self.request.user, 'player')):
            redirect_uri = urllib.urlencode({
                'redirect_uri':
                'http://' + self.request.get_host() + reverse("wechat_oauth2") + '?next=' + self.request.path})
            return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect' % (WX_APPID, redirect_uri))
        return super(BaseWeixinView, self).dispatch(*args, **kwargs)


class GameView(BaseWeixinView):

    def get(self, request):
        ctx = RequestContext(request, {})
        return render_to_response('games.html', ctx)


class GameJoinView(BaseWeixinView):

    def get(self, request, gid):
        assert (request.user.player is not None)
        game = get_object_or_404(Game, id=gid)
        pos = request.GET.get('pos')
        try:
            for i in ['red_van', 'red_rear', 'blue_van', 'blue_rear']:
                if getattr(game, i) == request.user.player:
                    setattr(game, i, None)
                    break
            player = getattr(game, pos)
            if not player:
                setattr(game, pos, request.user.player)
                game.save()
        except AttributeError:
            game.save()
        return HttpResponse('')


class GameDetailView(BaseWeixinView):

    def get(self, request, gid):
        game = get_object_or_404(Game, id=gid)
        gw_user = request_gw_user(
            settings.GW_APPID, settings.GW_USER, settings.GW_PWD)
        gw_obj = {'appid': settings.GW_APPID,
                  'uid': gw_user['uid'], 'token': gw_user['token']}
        ctx = {'game': game, 'gw_obj': gw_obj, 'foosball_obj': game.foosball}
        ctx = RequestContext(request, ctx)
        return render_to_response('game_%s.html' % game.get_status_display(), ctx)


class GameStartView(BaseWeixinView):

    def get(self, request, gid):
        game = get_object_or_404(Game, id=gid)
        for i in ['red_van', 'red_rear', 'blue_van', 'blue_rear']:
            if not getattr(game, i):
                return redirect(reverse('game_detail', kwargs={'gid': game.id}))
        if (game.status == Game.Status.waiting.value) and (
                request.user.player in [game.red_rear, game.red_van, game.blue_rear, game.blue_van]):
            game.status = Game.Status.playing.value
            game.save()

        return redirect(reverse('game_detail', kwargs={'gid': game.id}))


class GameEndView(BaseWeixinView):

    def get(self, request, gid):
        game = get_object_or_404(Game, id=gid)
        if (game.status == Game.Status.playing.value) and (
                request.user.player in [game.red_rear, game.red_van, game.blue_rear, game.blue_van]):
            game.status = Game.Status.end.value
            game.save()

        return redirect(reverse('game_detail', kwargs={'gid': game.id}))

    def post(self, request, gid):
        game = get_object_or_404(Game, id=gid)
        if (game.status == Game.Status.playing.value) and (
                request.user.player in [game.red_rear, game.red_van, game.blue_rear, game.blue_van]):
            game.red_score = request.POST.get('red_score', 0)
            game.blue_score = request.POST.get('blue_score', 0)
            game.status = Game.Status.end.value
            game.save()

        return redirect(reverse('game_detail', kwargs={'gid': game.id}))


class GameHistoryView(BaseWeixinView):

    def get(self, request):
        query = Q(status=Game.Status.end.value)
        player = request.GET.get('player')
        if player:
            player = int(player)
            query &= (Q(red_van__id=player) | Q(red_rear__id=player) | Q(
                blue_van__id=player) | Q(blue_rear__id=player))

        games = Game.objects.filter(query).order_by('-updated_at')
        page = request.GET.get('page', 1)
        page_count = 10
        games = dj_simple_pagination(games, page, page_count)
        return render_to_response('game_history.html', {'games': games, 'page': page})


class PlayerView(BaseWeixinView):

    def get(self, request):
        players = []
        for i in Player.objects.all():
            win, lost = i.performance()
            players.append((i, win, lost))
        players = sorted(players, key=lambda x: x[2])
        players = sorted(players, key=lambda x: x[1], reverse=True)
        players = map(lambda pl:{'rank':pl[0], 'player': pl[1]}, enumerate(players))  # [player,player, ...] --> [{rank:player}, {rank:player}]
        page = request.GET.get('page', 1)
        page_count = 10
        players = dj_simple_pagination(players, page, page_count)
        ctx = {'players': players, 'page': page}
        return render_to_response('players.html', ctx)


class MeView(BaseWeixinView):

    def get(self, request):
        me = request.user.player
        win, lost = me.performance()
        performances = []
        for i in Player.objects.all():
            w, l = i.performance()
            performances.append((i, w, l))
        performances = sorted(performances, key=lambda x: x[2])
        performances = sorted(performances, key=lambda x: x[1], reverse=True)
        ctx = RequestContext(
            request,
            {"win": win,
             "lost": lost,
             "tot_players": len(performances),
             "rank": performances.index((me, win, lost)) + 1,
             "partners": me.partners()})
        return render_to_response('me.html', ctx)


class GameScoreView(View):

    def get(self, request, gid):
        game = get_object_or_404(Game, id=gid)
        return render_json_response({"red_score": game.red_score, "blue_score": game.blue_score})


def render_json_response(ret, status=200, headers={}):
    #    resp = HttpResponse(json.dumps(ret), status=status, mimetype='application/json')
    # i don't know why, but it just work
    resp = HttpResponse(
        json.dumps(ret), status=status,  content_type='application/json')
    for k, v in headers.items():
        resp[k] = v
    return resp


def wechat_oauth2(request):
    code = request.GET.get('code')
    if code:
        params = {'appid': WX_APPID,
                  'secret': WX_SECRET,
                  'code': code,
                  'grant_type': 'authorization_code'}
        try:
            resp = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token',
                                params=params)
            tokens = json.loads(resp.content)
            openid = tokens['openid']
            params = {'access_token': tokens['access_token'],
                      'openid': openid,
                      'lang': 'zh_CN'}
            resp = requests.get(
                'https://api.weixin.qq.com/sns/userinfo', params=params)
            user = json.loads(resp.content)
            try:
                u = User.objects.get(username=openid[:30])
            except User.DoesNotExist:
                u = User(username=openid[:30])
                u.set_password(openid[:8])
                u.save()
            au = authenticate(username=openid[:30], password=openid[:8])
            login(request, au)
            try:
                p = Player.objects.get(openid=openid)
                p.access_token = tokens['access_token']
                p.expires_at = tokens['expires_in']
                p.scope = tokens['scope']
                p.nickname = user['nickname']
                p.headimgurl = user['headimgurl']
                p.user = u
                p.save()
            except Player.DoesNotExist:
                p = Player(openid=openid,
                           access_token=tokens['access_token'],
                           expires_at=tokens['expires_in'],
                           refresh_token=tokens['refresh_token'],
                           scope=tokens['scope'],
                           nickname=user['nickname'],
                           headimgurl=user['headimgurl'],
                           user=u)
                p.save()
        except Exception, e:
            logger.exception(e)
            return HttpResponse("authorize failed")
    return redirect(request.GET.get('next'))


def qrcode(request):
    mac = request.GET.get('mac')
    fb = get_object_or_404(FoosBall, mac__iexact=mac)
    qrcode = get_qrcode(fb.scene_id)
    return HttpResponse('<img src="%s%s" />' % (settings.MEDIA_URL, qrcode))
