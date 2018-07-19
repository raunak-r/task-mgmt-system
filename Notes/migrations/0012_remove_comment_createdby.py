# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0011_comment_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='createdBy',
        ),
        migrations.RenameField(
        	model_name='comment',
        	old_name='user',
        	new_name='createdBy',
        ),
    ]
