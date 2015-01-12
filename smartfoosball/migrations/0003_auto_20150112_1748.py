# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('smartfoosball', '0002_auto_20141223_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='access_token',
            field=models.CharField(max_length=256, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='expires_at',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='headimgurl',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='nickname',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='refresh_token',
            field=models.CharField(max_length=256, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='scope',
            field=models.CharField(max_length=256, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
