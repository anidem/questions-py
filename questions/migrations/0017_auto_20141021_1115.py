# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0016_auto_20141021_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionquestion',
            name='slug',
            field=models.SlugField(default='slugme'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='slug',
            field=models.SlugField(default='slugme'),
            preserve_default=False,
        ),
    ]
