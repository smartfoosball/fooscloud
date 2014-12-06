# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('red_score', models.IntegerField(default=0)),
                ('blue_score', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=1, choices=[(0, b'unknown'), (1, b'waiting'), (2, b'playing'), (3, b'end')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('position', models.IntegerField(choices=[(0, b'unknown'), (1, b'red_van'), (2, b'red_rear'), (3, b'blue_van'), (4, b'blue_rear')])),
                ('team', models.IntegerField(choices=[(0, b'unknown'), (1, b'red'), (2, b'blue')])),
                ('game', models.ForeignKey(to='smartfoosball.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('openid', models.CharField(max_length=32)),
                ('access_token', models.CharField(max_length=256)),
                ('expires_at', models.IntegerField()),
                ('refresh_token', models.CharField(max_length=256)),
                ('scope', models.CharField(max_length=256)),
                ('nickname', models.CharField(max_length=128)),
                ('headimgurl', models.URLField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='goal',
            name='player',
            field=models.ForeignKey(to='smartfoosball.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='blue_rear',
            field=models.ForeignKey(related_name='blue_rear_games', blank=True, to='smartfoosball.Player', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='blue_van',
            field=models.ForeignKey(related_name='blue_van_games', blank=True, to='smartfoosball.Player', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='red_rear',
            field=models.ForeignKey(related_name='red_rear_games', blank=True, to='smartfoosball.Player', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='red_van',
            field=models.ForeignKey(related_name='red_van_games', blank=True, to='smartfoosball.Player', null=True),
            preserve_default=True,
        ),
    ]
