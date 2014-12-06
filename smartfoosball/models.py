from django.db import models


class Player(models.Model):
    openid = models.CharField(max_length=32)
    access_token = models.CharField(max_length=32)
    expires_at = models.IntegerField()
    refresh_token = models.CharField(max_length=32)
    scope = models.CharField(max_length=256)
    nickname = models.CharField(max_length=128)
    headimgurl = models.URLField()

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
