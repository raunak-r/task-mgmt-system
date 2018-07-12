# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentId', models.AutoField(serialize=False, primary_key=True)),
                ('createdOn', models.DateTimeField(auto_now_add=True)),
                ('UpdatedOn', models.DateTimeField(auto_now_add=True)),
                ('createdBy', models.CharField(max_length=10)),
                ('commentText', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['createdBy'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('taskId', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100, blank=True)),
                ('label', models.CharField(max_length=1, choices=[(b'1', b'Todo'), (b'2', b'Doing'), (b'3', b'Done')])),
                ('color', models.CharField(blank=True, max_length=7, choices=[(b'#808080', b'Gray'), (b'#000000', b'Black'), (b'#FF0000', b'Red'), (b'#0000FF', b'Blue')])),
                ('comments', models.CharField(max_length=255, blank=True)),
                ('createdBy', models.CharField(max_length=10)),
                ('dueDate', models.DateField()),
            ],
            options={
                'ordering': ['-dueDate'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='taskId',
            field=models.ForeignKey(to='Notes.Task'),
        ),
    ]
