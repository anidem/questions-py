# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('questions', '0013_auto_20141021_0907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='optionquestion',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='optionquestion',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='textquestion',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='textquestion',
            name='object_id',
        ),
    ]
