# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('questions', '0018_auto_20141026_0829'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionSequence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionSequenceItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('question_sequence', models.ForeignKey(to='questions.QuestionSequence')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
