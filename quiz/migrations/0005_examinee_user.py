# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-06-15 12:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0004_classroom_examinee'),
    ]

    operations = [
        migrations.AddField(
            model_name='examinee',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
