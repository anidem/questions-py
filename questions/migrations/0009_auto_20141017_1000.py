# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20141017_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textquestion',
            name='input_size',
            field=models.CharField(default=b'short', max_length=64, choices=[(b'1', b'short answer (1 row 80 cols)'), (b'5', b'5 rows 80 cols'), (b'40', b'long input (40 rows 80 cols)')]),
        ),
    ]
