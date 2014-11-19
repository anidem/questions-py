# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0023_questionresponse'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuestionSequence',
            new_name='QuestionSet',
        ),
        migrations.RemoveField(
            model_name='optionquestionresponse',
            name='question',
        ),
        migrations.RemoveField(
            model_name='optionquestionresponse',
            name='response',
        ),
        migrations.RemoveField(
            model_name='optionquestionresponse',
            name='user',
        ),
        migrations.DeleteModel(
            name='OptionQuestionResponse',
        ),
        migrations.RemoveField(
            model_name='textquestionresponse',
            name='question',
        ),
        migrations.RemoveField(
            model_name='textquestionresponse',
            name='user',
        ),
        migrations.DeleteModel(
            name='TextQuestionResponse',
        ),
        migrations.AlterModelOptions(
            name='questionsequenceitem',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='questionsequenceitem',
            name='question_sequence',
            field=models.ForeignKey(related_name=b'sequence_items', to='questions.QuestionSet'),
        ),
        migrations.AlterField(
            model_name='textquestion',
            name='input_size',
            field=models.CharField(default=b'1', max_length=64, choices=[(b'1', b'short answer: (1 row 80 cols)'), (b'5', b'sentence: (5 rows 80 cols'), (b'15', b'paragraph(s): (15 rows 80 cols)')]),
        ),
    ]
