# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartfoosball', '0001_initial'),
    ]

    operations = [
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
    ]
