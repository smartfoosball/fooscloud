from django import forms
from django.http import HttpResponse
from django.views.generic import View,TemplateView
from django.shortcuts import render_to_response
from datetime import datetime
from django.conf import settings
from models import *
from helper import *
from foosball_config import *
from smartfoosball.settings import *

import time
import json
import uuid


class Index(TemplateView):
    template_name = 'index.html'
    def get(self, request):
        return super(Index, self).get(request)


class PlayerRegister(View):
    def get(self, request, nick_name):
        _nick_name = str(nick_name)
        _player_auth_sn=str(uuid.uuid4())
        p = Players(wechat_id='', auth_sn=_player_auth_sn, nick_name=_nick_name)
        p.save()
        return HttpResponse(_player_auth_sn)


class GameCreate(View):
    def get(self, request, auth_sn):
        # create game
        _game_id = str(uuid.uuid4())
        print _game_id
        game_model = Games(game_id=_game_id,
                           game_status=GameStatusEn.waiting.value,
                           creater_sn=get_player_by_auth(str(auth_sn)),
                           created_at=datetime.now()
                           )
        game_model.save(force_insert=True)
        #create position
        generate_position_blank(game_model)

        return HttpResponse(_game_id)


class GamePosition(View):
    def get(self, request, game_id, auth_sn, team_id, position_id):
        _game_id = str(game_id)
        _game_sn = gameid_to_gamesn(_game_id)
        _auth_sn = str(auth_sn)
        _team_id = int(team_id)
        _position_id = int(position_id)
        print _game_sn
        pos = Positions.objects.filter(game_sn=_game_sn,
                                       team_id=_team_id,
                                       pos_id=_position_id,
                                       ).first()
        if pos:
            if pos.player_sn.sn == god_player_sn():
                pos.player_sn = get_player_by_auth(_auth_sn)
                pos.save()
                return HttpResponse('OK')
            else:
                return HttpResponse('player_exists')
        else:
            return HttpResponse('Position Not found')


class GameScore(TemplateView):
    template_name = 'score_board.html'

    def get(self, request, game_id):
        '''
        struct:
        {
        'game_id':str,
        'teams':{1:{1:player_object, 2:player_object}, 2:{1:player_obj,2:player_obj}},
        
        }
        '''
#        return render_to_response(self.template_name)
        gsn = get_game_by_game_id(game_id)
        score_struct = {'game_id': game_id}
        teams = {TeamEn.red.name: None, TeamEn.blue.name: None}
        if gsn:
            pos = Positions.objects.filter(game_sn=gsn).all()
            # red
            teams[TeamEn.red.name] = {PositionEn.attack.name:get_player(pos, TeamEn.red.value, PositionEn.attack.value)}
            teams[TeamEn.red.name].update({PositionEn.defence.name:get_player(pos, TeamEn.red.value, PositionEn.defence.value)})
            # blue
            teams[TeamEn.blue.name] = {PositionEn.attack.name:get_player(pos, TeamEn.blue.value, PositionEn.attack.value)}
            teams[TeamEn.blue.name].update({PositionEn.defence.name:get_player(pos, TeamEn.blue.value, PositionEn.defence.value)})
        score_struct = {'teams':teams}
        return render_to_response('score_board.html', {"score_board":score_struct})
        

# from __future__ import absolute_import, unicode_literals
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy.enterprise import parse_message, create_reply


class WechatEcho(View):
    def get(self, request):
        signature = request.GET.get('msg_signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')

        crypto = WeChatCrypto(TOKEN, EncodingAESKey, CorpId)
        echo_str = request.GET.get('echostr', '')
        try:
            echo_str = crypto.check_signature(
                signature,
                timestamp,
                nonce,
                echo_str
            )
        except InvalidSignatureException:
            return HttpResponse(status=403)
        return HttpResponse(echo_str)
