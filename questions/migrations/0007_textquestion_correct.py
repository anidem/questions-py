# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_auto_20141016_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='textquestion',
            name='correct',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
