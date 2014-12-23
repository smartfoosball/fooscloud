# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartfoosball', '0002_gwuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoosBall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('scene_id', models.IntegerField()),
                ('mac', models.CharField(max_length=12)),
                ('did', models.CharField(max_length=32, null=True, blank=True)),
                ('passcode', models.CharField(max_length=32, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
