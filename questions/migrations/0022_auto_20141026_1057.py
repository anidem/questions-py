# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0021_auto_20141026_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionsequence',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
