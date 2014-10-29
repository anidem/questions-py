# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0017_auto_20141021_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='optionquestion',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='textquestion',
            name='slug',
        ),
    ]
