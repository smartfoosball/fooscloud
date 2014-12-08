from django import forms
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.views.generic import View,TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
from models import *
from helper import *
from foosball_config import *
from smartfoosball.settings import *
from smartfoosball.models import *
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.messages import TextMessage
from wechatpy.replies import TextReply
from wechatpy import parse_message

import time
import json
import uuid
import urllib
import requests

class Index(TemplateView):
    template_name = 'index.html'
    def get(self, request):
        return super(Index, self).get(request)
        

class WechatEcho(View):

    def get(self, request):
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')

        try:
            check_signature(TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            return HttpResponse(status=403)
        return HttpResponse(echo_str)

    def post(self, request):
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')

        try:
            check_signature(TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            return HttpResponse(status=403)

        msg = parse_message(request.body)
        reply = TextReply(content='I got it!', message=msg)
        return HttpResponse(reply.render())


class BaseWeixinView(View):

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            redirect_uri = urllib.urlencode({
                    'redirect_uri':
                        'http://' + self.request.get_host() + reverse("wechat_oauth2")})
            return redirect('https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect' % (WX_APPID, redirect_uri))
        return super(BaseWeixinView, self).dispatch(*args, **kwargs)


class GameView(BaseWeixinView):

    def get(self, request):
        playing = Game.objects.filter(status=Game.Status.playing.value).first()
        waiting = Game.objects.filter(status=Game.Status.waiting.value).first()
        if not waiting:
            waiting = Game()
            waiting.save()
        ctx = {'playing': playing, 'waiting': waiting}
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
        ctx = {'game': game}
        ctx = RequestContext(request, ctx)
        return render_to_response('game_%s.html' % game.get_status_display(), ctx)


class GameStartView(BaseWeixinView):

    def get(self, request, gid):
        game = get_object_or_404(Game, id=gid)
        ctx = {'game': game}
        for i in ['red_van', 'red_rear', 'blue_van', 'blue_rear']:
            if not getattr(game, i):
                return redirect(reverse('game_detail', kwargs={'gid': game.id}))
        playing = Game.objects.filter(status=Game.Status.playing.value).first()
        if (not playing) and (game.status == Game.Status.waiting.value) and (
            request.user.player in [game.red_rear, game.red_van, game.blue_rear, game.blue_van]):
            game.status = Game.Status.playing.value
            game.save()

        return redirect(reverse('game_detail', kwargs={'gid': game.id}))


class GameEndView(BaseWeixinView):
    
    def get(self, request, gid):
        game = get_object_or_404(Game, id=gid)
        ctx = {'game': game}
        if (game.status == Game.Status.playing.value) and (
            request.user.player in [game.red_rear, game.red_van, game.blue_rear, game.blue_van]):
            game.status = Game.Status.end.value
            game.save()

        return redirect(reverse('game_detail', kwargs={'gid': game.id}))


class GameHistoryView(BaseWeixinView):
    
    def get(self, request):
        query = Q(status=Game.Status.end.value)
        player = request.GET.get('player')
        if player:
            player = int(player)
            query &= (Q(red_van__id=player) | Q(red_rear__id=player) | Q(blue_van__id=player) | Q(blue_rear__id=player))
        games = Game.objects.filter(query).order_by('-updated_at')[:10]
        return render_to_response('game_history.html', {'games': games})


class PlayerView(BaseWeixinView):

    def get(self, request):
        players = []
        for i in Player.objects.all():
            win, lost = i.performance()
            players.append((i, win, lost))
        players = sorted(players, key=lambda x: x[2])
        players = sorted(players, key=lambda x: x[1], reverse=True)
        ctx = {'players': players}
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


def wechat_oauth2(request):
    code = request.GET.get('code')
    if code:
        params={'appid': WX_APPID,
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
            resp = requests.get('https://api.weixin.qq.com/sns/userinfo', params=params)
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
            return HttpResponse("authorize failed")
    return redirect(reverse("me"))
