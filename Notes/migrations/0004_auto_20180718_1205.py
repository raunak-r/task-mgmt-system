# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0003_auto_20180718_1200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='is_deleted',
            new_name='is_active',
        ),
    ]
