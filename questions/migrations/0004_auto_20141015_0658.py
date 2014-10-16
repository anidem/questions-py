# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_optionquestionresponse_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='optionquestionresponse',
            old_name='response',
            new_name='option_response',
        ),
    ]
