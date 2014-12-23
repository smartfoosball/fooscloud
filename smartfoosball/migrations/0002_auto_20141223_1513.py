# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartfoosball', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoosBall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('scene_id', models.IntegerField()),
                ('mac', models.CharField(unique=True, max_length=12)),
                ('did', models.CharField(max_length=32, null=True, blank=True)),
                ('passcode', models.CharField(max_length=32, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GWUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.CharField(max_length=32)),
                ('token', models.CharField(max_length=32)),
                ('expire_at', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='game',
            name='foosball',
            field=models.ForeignKey(blank=True, to='smartfoosball.FoosBall', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='foosball',
            field=models.ManyToManyField(to='smartfoosball.FoosBall'),
            preserve_default=True,
        ),
    ]
