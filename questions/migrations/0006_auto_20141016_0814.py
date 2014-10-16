# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_auto_20141016_0744'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='textquestion',
            options={'ordering': ['display_order']},
        ),
        migrations.AddField(
            model_name='textquestion',
            name='display_order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='display_text',
            field=models.TextField(default='question text'),
            preserve_default=False,
        ),
    ]
