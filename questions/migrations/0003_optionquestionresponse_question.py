# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20141010_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='optionquestionresponse',
            name='question',
            field=models.ForeignKey(default=1, to='questions.OptionQuestion'),
            preserve_default=False,
        ),
    ]
