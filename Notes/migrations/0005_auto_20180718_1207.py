# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0004_auto_20180718_1205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='is_active',
            new_name='isActive',
        ),
    ]
