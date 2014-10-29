# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_auto_20141017_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_text', models.TextField()),
                ('display_order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['display_order'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='optionquestion',
            options={},
        ),
        migrations.AlterModelOptions(
            name='textquestion',
            options={},
        ),
        migrations.RemoveField(
            model_name='optionquestion',
            name='display_order',
        ),
        migrations.RemoveField(
            model_name='optionquestion',
            name='display_text',
        ),
        migrations.RemoveField(
            model_name='optionquestion',
            name='id',
        ),
        migrations.RemoveField(
            model_name='textquestion',
            name='display_order',
        ),
        migrations.RemoveField(
            model_name='textquestion',
            name='display_text',
        ),
        migrations.RemoveField(
            model_name='textquestion',
            name='id',
        ),
        migrations.AddField(
            model_name='optionquestion',
            name='abstractquestion_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='questions.AbstractQuestion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='abstractquestion_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default=1, serialize=False, to='questions.AbstractQuestion'),
            preserve_default=False,
        ),
    ]
