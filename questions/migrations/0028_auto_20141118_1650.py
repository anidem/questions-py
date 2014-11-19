# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0027_auto_20141118_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionquestion',
            name='display_image',
            field=models.FileField(null=True, upload_to=b'img', blank=True),
        ),
        migrations.AlterField(
            model_name='textquestion',
            name='display_image',
            field=models.FileField(null=True, upload_to=b'img', blank=True),
        ),
    ]
