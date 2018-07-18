# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0008_auto_20180718_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='createdBy',
        ),
    ]
