# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartfoosball', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='access_token',
            field=models.CharField(max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='refresh_token',
            field=models.CharField(max_length=256),
            preserve_default=True,
        ),
    ]
