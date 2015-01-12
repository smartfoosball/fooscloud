from enum import Enum
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class Enumm(Enum):

    @classmethod
    def choices(cls):
        choices = []
        for i in cls:
            choices.append((i.value, i.name))
        return tuple(choices)


class FoosBall(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    scene_id = models.IntegerField()
    mac = models.CharField(max_length=12, unique=True)
    did = models.CharField(max_length=32, blank=True, null=True)
    passcode = models.CharField(max_length=32, blank=True, null=True)

    def __unicode__(self):
        return self.mac

    def get_game(self):
        playing = self.game_set.filter(status=Game.Status.playing.value).first()
        if playing:
            return playing

        waiting = self.game_set.filter(status=Game.Status.waiting.value).first()
        if waiting:
            return waiting

        game = Game(foosball=self)
        game.save()
        return game

class Player(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    openid = models.CharField(max_length=32)
    access_token = models.CharField(max_length=256, null=True, blank=True)
    expires_at = models.IntegerField(null=True, blank=True)
    refresh_token = models.CharField(max_length=256, null=True, blank=True)
    scope = models.CharField(max_length=256, null=True, blank=True)
    nickname = models.CharField(max_length=128, null=True, blank=True)
    headimgurl = models.URLField(null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True)
    foosball = models.ManyToManyField(FoosBall)

    def __unicode__(self):
        return self.nickname

    def partners(self):
        query = (Q(red_van=self) | Q(red_rear=self) | Q(blue_van=self) | Q(blue_rear=self)) & Q(status=Game.Status.end.value)
        games = Game.objects.filter(query)
        ret = set()
        for i in games:
            if i.red_van == self:
                ret.add(i.red_rear)
            elif i.red_rear == self:
                ret.add(i.red_van)
            elif i.blue_van == self:
                ret.add(i.blue_rear)
            elif i.blue_rear == self:
                ret.add(i.blue_van)
        if None in ret:
            ret.remove(None)
        return ret

    def performance(self):
        query = (Q(red_van=self) | Q(red_rear=self) | Q(blue_van=self) | Q(blue_rear=self)) & Q(status=Game.Status.end.value)
        games = Game.objects.filter(query)
        win, lost = 0, 0
        for i in games:
            if (i.red_van == self) or (i.red_rear == self):
                if i.red_score > i.blue_score:
                    win += 1
                else:
                    lost += 1
            else:
                if i.red_score > i.blue_score:
                    lost += 1
                else:
                    win += 1
        return win, lost


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
    foosball = models.ForeignKey(FoosBall, blank=True, null=True)

    def __unicode__(self):
        return u"%s-%s vs %s-%s" % (self.red_van, self.red_rear, 
                                   self.blue_van, self.blue_rear)

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


class GWUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uid = models.CharField(max_length=32)
    token = models.CharField(max_length=32)
    expire_at = models.IntegerField()

