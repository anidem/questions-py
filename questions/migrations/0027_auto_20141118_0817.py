# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0026_auto_20141118_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionquestion',
            name='display_image',
            field=models.FileField(null=True, upload_to=b'/media/img/', blank=True),
        ),
        migrations.AlterField(
            model_name='textquestion',
            name='display_image',
            field=models.FileField(null=True, upload_to=b'/media/img/', blank=True),
        ),
    ]
