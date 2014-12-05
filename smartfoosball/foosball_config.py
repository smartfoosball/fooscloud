#coding:utf-8
'''
foosball with wechat, base on sqlite3

databse struct
tb: games
column:
sn:int, index
game_id:string, uuid
game_status:int, lookup GameStatusEn
creater_id:int, tb_player_id
created_at:int, timestamp
===

tb:positions (it can for analytic)
column:
sn:int, index
game_id:string, tb_game_id
team_id:int, lookup TeamEn
pos_id:int, lookup PositionEn
player_id:int, tb_player_id
==

tb:players
column:
sn:index
wechat_id:string, wechat openid
nick_name:string, username
'''

from enum import Enum

class GameStatusEn(Enum):
    unknow = 0
    waiting = 1
    playing = 2
    end = 3


class TeamEn(Enum):
    unknow = 0
    red = 1
    blue = 2


class PositionEn(Enum):
    unknow = 0
    attack = 1
    defence = 2
