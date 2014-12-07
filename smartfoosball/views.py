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
        '''
        {
        'game_id':str,
        'teams':{1:{1:player_object, 2:player_object}, 2:{1:player_obj,2:player_obj}},
        }
        {
            "games":[{game_id:str, teams:{...}}]
        }
        '''
        playing = Game.objects.filter(status=Game.Status.playing.value).first()
        waiting = Game.objects.filter(status=Game.Status.waiting.value).first()
        if (not playing) and (not waiting):
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
        return redirect(reverse('games'))


class GameDetailView(BaseWeixinView):

    def get(self, request, gid):
        game = get_object_or_404(Game, id=gid)
        ctx = {'game': game}
        return render_to_response('game_detail.html', ctx)


class GameStartView(BaseWeixinView):

    def get(self, request, gid):
        game = get_object_or_404(Game, id=gid)
        ctx = {'game': game}
        for i in ['red_van', 'red_rear', 'blue_van', 'blue_rear']:
            if not getattr(game, i):
                return render_to_response('game_detail.html', ctx)
        playing = Game.objects.filter(status=Game.Status.playing.value).first()
        if not playing:
            game.status = Game.Status.playing.value
            game.save()
        return render_to_response('game_detail.html', ctx)


class GameEndView(BaseWeixinView):
    
    def get(self, request, gid):
        game = get_object_or_404(Game, id=gid)
        ctx = {'game': game}
        game.status = Game.Status.end.value
        game.save()
        return render_to_response('game_detail.html', ctx)


class GameHistoryView(BaseWeixinView):
    
    def get(self, request):
        return render_to_response(
            'game_history.html', 
            {'games': Game.objects.filter(status=Game.Status.end.value).order_by('-updated_at')[:10]})


class PlayerView(View):

    def get(self, request):
        return render_to_response('players.html', {'something':"1"})


class MeView(BaseWeixinView):

    def get(self, request):
        me = request.user.player
        win, lost = me.performance()
        performances = []
        for i in Player.objects.all():
            performances.append((i, i.performance()[0]))
        sorted(performances, key=lambda x: x[1], reverse=True)
        ctx = RequestContext(
            request, 
            {"win": win, 
             "lost": lost,
             "tot_players": len(performances),
             "rank": performances.index((me, win)) + 1,
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
