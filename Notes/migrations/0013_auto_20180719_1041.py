# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0012_remove_comment_createdby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='createdBy',
            field=models.ForeignKey(to='Notes.User'),
        ),
        migrations.AlterField(
            model_name='task',
            name='createdBy',
            field=models.ForeignKey(to='Notes.User'),
        ),
    ]
