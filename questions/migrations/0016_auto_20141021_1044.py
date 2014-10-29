# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0015_question_display_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
