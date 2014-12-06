from enum import Enum
from django.db import models
from django.contrib.auth.models import User


class Enumm(Enum):

    @classmethod
    def choices(cls):
        choices = []
        for i in cls:
            choices.append((i.value, i.name))
        return tuple(choices)


class Player(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    openid = models.CharField(max_length=32)
    access_token = models.CharField(max_length=256)
    expires_at = models.IntegerField()
    refresh_token = models.CharField(max_length=256)
    scope = models.CharField(max_length=256)
    nickname = models.CharField(max_length=128)
    headimgurl = models.URLField()
    user = models.OneToOneField(User)


class Game(models.Model):
    
    class Status(Enumm):
        unknown = 0
        waiting = 1
        playing = 2
        end = 3

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    red_van  = models.ForeignKey(Player, related_name='red_van_games', blank=True, null=True)
    red_rear = models.ForeignKey(Player, related_name='red_rear_games', blank=True, null=True)
    blue_van = models.ForeignKey(Player, related_name='blue_van_games', blank=True, null=True)
    blue_rear = models.ForeignKey(Player, related_name='blue_rear_games', blank=True, null=True)
    red_score = models.IntegerField(default=0)
    blue_score = models.IntegerField(default=0)
    status = models.IntegerField(choices=Status.choices(), default=Status.waiting.value)


class Goal(models.Model):

    class Position(Enumm):
        unknown = 0
        red_van = 1
        red_rear = 2
        blue_van = 3
        blue_rear = 4

    class Team(Enumm):
        unknown = 0
        red = 1
        blue = 2

    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    position = models.IntegerField(choices=Position.choices())
    team = models.IntegerField(choices=Team.choices())
    

# class Games(models.Model):
# #    sn = models.IntegerField(primary_key=True)
#     sn = models.AutoField(primary_key=True)
#     game_id = models.CharField(max_length=100)
#     game_status = models.IntegerField(blank=True, null=True)
#     creater_sn = models.ForeignKey('Players', db_column='creater_sn', blank=True, null=True)
#     created_at = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'games'


# class Players(models.Model):
#     sn = models.AutoField(primary_key=True)
#     wechat_id = models.CharField(max_length=100, blank=True)
#     auth_sn = models.CharField(max_length=100, blank=True)
#     nick_name = models.CharField(max_length=50, blank=True)

#     class Meta:
#         managed = False
#         db_table = 'players'


# class Positions(models.Model):
#     sn = models.AutoField(primary_key=True)
#     game_sn = models.ForeignKey(Games, db_column='game_sn', blank=True, null=True)
#     team_id = models.IntegerField(blank=True, null=True)
#     pos_id = models.IntegerField(blank=True, null=True)
#     player_sn = models.ForeignKey(Players, db_column='player_sn', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'positions'
