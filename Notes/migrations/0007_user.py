# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0006_auto_20180718_1244'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
    ]
