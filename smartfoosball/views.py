from django import forms
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from datetime import datetime
from django.conf import settings

import time
import json


class Index(TemplateView):
    template_name = 'index.html'
    def get(self, request):
        return super(Index, self).get(request)



class GameScore(TemplateView):
    template_name = 'score_board.html'

#     def post(self, request):
#         return super(WiFiView, self).get(request)
    
    def get(self, request, game_id):
        '''
        struct:
        {
        'game_id':str,
        'teams':{1:{1:player_object, 2:player_object}, 2:{1:player_obj,2:player_obj}},
        
        }
        '''
        return render_to_response(self.template_name)
        gsn = gameid_to_gamesn(game_id)
        score_struct = {'game_id': game_id}
        teams = {TeamEn.red.name: None, TeamEn.blue.name: None}
        if gsn:
            pos = web.ctx.orm.query(Position).filter(Position.game_sn==gsn).all()
            # red
            teams[TeamEn.red.name] = {PositionEn.attack.name:get_player(pos, TeamEn.red.value, PositionEn.attack.value)}
            teams[TeamEn.red.name].update({PositionEn.defence.name:get_player(pos, TeamEn.red.value, PositionEn.defence.value)})
            # blue
            teams[TeamEn.blue.name] = {PositionEn.attack.name:get_player(pos, TeamEn.blue.value, PositionEn.attack.value)}
            teams[TeamEn.blue.name].update({PositionEn.defence.name:get_player(pos, TeamEn.blue.value, PositionEn.defence.value)})
        
        score_struct = {'teams':teams}
        return render_db.score_board(score_board=score_struct)
        
