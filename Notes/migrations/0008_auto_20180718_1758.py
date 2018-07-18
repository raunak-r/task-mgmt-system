# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0007_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username']},
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(to='Notes.User', null=True),
        ),
    ]
