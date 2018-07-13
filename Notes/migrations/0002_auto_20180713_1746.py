# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['taskId_id']},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['dueDate']},
        ),
        migrations.AddField(
            model_name='task',
            name='attachment',
            field=models.FileField(upload_to=b'attachments', blank=True),
        ),
    ]
