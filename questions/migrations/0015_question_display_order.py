# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0014_auto_20141021_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='display_order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
