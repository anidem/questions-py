# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_textquestion_correct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textquestion',
            name='input_size',
            field=models.CharField(default=b'short', max_length=64, choices=[(b'short', b'short answer (40 characters)'), (b'sentence', b'5 rows 80 cols'), (b'paragraphs', b'long input (40 rows 80 cols)')]),
        ),
    ]
