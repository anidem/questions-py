# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0020_auto_20141026_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionsequence',
            name='slug',
            field=models.SlugField(default=datetime.date(2014, 10, 26)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='questionsequenceitem',
            name='question_sequence',
            field=models.ForeignKey(related_name=b'questions', to='questions.QuestionSequence'),
        ),
    ]
