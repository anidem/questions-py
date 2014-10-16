# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='option',
            name='question',
            field=models.ForeignKey(related_name=b'options', to='questions.OptionQuestion'),
        ),
        migrations.AlterField(
            model_name='optionquestion',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
    ]
