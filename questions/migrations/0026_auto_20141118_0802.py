# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0025_auto_20141111_2334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='option',
            options={'ordering': ['display_order', 'id']},
        ),
        migrations.AlterModelOptions(
            name='questionsequenceitem',
            options={},
        ),
        migrations.RemoveField(
            model_name='questionsequenceitem',
            name='order',
        ),
        migrations.AddField(
            model_name='optionquestion',
            name='display_image',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='display_image',
            field=models.FileField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
