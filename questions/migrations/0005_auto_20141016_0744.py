# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20141015_0658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='optionquestionresponse',
            old_name='option_response',
            new_name='response',
        ),
        migrations.AddField(
            model_name='textquestionresponse',
            name='question',
            field=models.ForeignKey(default=1, to='questions.TextQuestion'),
            preserve_default=False,
        ),
    ]
