# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('questions', '0011_auto_20141021_0717'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractquestion',
            name='content_type',
            field=models.ForeignKey(default=9, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='abstractquestion',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='textquestion',
            name='input_size',
            field=models.CharField(default=b'short', max_length=64, choices=[(b'1', b'short answer: (1 row 80 cols)'), (b'5', b'sentence: (5 rows 80 cols'), (b'15', b'paragraph(s): (15 rows 80 cols)')]),
        ),
    ]
