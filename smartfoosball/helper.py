#coding:utf-8
from models import *
from foosball_config import *


def god_player_sn():
    '''
    this player is not exists....just for blank
    '''
    return 1
def god_player():
    player = Players.objects.filter(sn=1).first()
    return player

def authsn_to_sn(auth_sn):
    player = Players.objects.filter(auth_sn=auth_sn).first()
    if player:
        return player.sn
    return None


def get_player_by_auth(auth_sn):
    player = Players.objects.filter(auth_sn=auth_sn).first()
    return player


def generate_position_blank(gsn):
    #red attack
    pos = Positions(game_sn=gsn,
                   team_id=TeamEn.red.value,
                   pos_id=PositionEn.attack.value,
                   player_sn=god_player()
                   )
    pos.save()
    # red defence
    pos = Positions(game_sn=gsn,
                   team_id=TeamEn.red.value,
                   pos_id=PositionEn.defence.value,
                   player_sn=god_player()
                   )
    pos.save()
    # blue attack
    pos = Positions(game_sn=gsn,
                   team_id=TeamEn.blue.value,
                   pos_id=PositionEn.attack.value,
                   player_sn=god_player()
                   )
    pos.save()
    # blue defence
    pos = Positions(game_sn=gsn,
                   team_id=TeamEn.blue.value,
                   pos_id=PositionEn.defence.value,
                   player_sn=god_player()
                   )
    pos.save()
    return True


def gameid_to_gamesn(game_id):
    game = Games.objects.filter(game_id=game_id, game_status=GameStatusEn.waiting.value).first()
    if game:
        return game.sn
    return None

def get_game_by_game_id(game_id):
    game = Games.objects.filter(game_id=game_id, game_status=GameStatusEn.waiting.value).first()
    return game
    

def get_player(pos, team_id, pos_id):
    assert len(pos)==4
    return [p for p in pos if p.team_id == team_id and p.pos_id == pos_id][0].player_sn
