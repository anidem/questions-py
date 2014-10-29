# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('questions', '0012_auto_20141021_0904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractquestion',
            name='content_type',
        ),
        migrations.AlterModelOptions(
            name='optionquestion',
            options={'ordering': ['display_order']},
        ),
        migrations.AlterModelOptions(
            name='textquestion',
            options={'ordering': ['display_order']},
        ),
        migrations.RemoveField(
            model_name='optionquestion',
            name='abstractquestion_ptr',
        ),
        migrations.RemoveField(
            model_name='textquestion',
            name='abstractquestion_ptr',
        ),
        migrations.DeleteModel(
            name='AbstractQuestion',
        ),
        migrations.AddField(
            model_name='optionquestion',
            name='content_type',
            field=models.ForeignKey(default=1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='optionquestion',
            name='display_order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='optionquestion',
            name='display_text',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='optionquestion',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='optionquestion',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='content_type',
            field=models.ForeignKey(default=1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='display_order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='display_text',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textquestion',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
