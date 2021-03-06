# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-08-26 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='coin',
            field=models.IntegerField(null=True, verbose_name='金币'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女'), ('other', '其他')], default='other', max_length=6),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.IntegerField(null=True, verbose_name='学院'),
        ),
    ]
