# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-21 23:51
from __future__ import unicode_literals

import db_comments.model_mixins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0081_fuelcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuelCodeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('display_order', models.IntegerField()),
                ('status', models.CharField(blank=True, max_length=25, null=True, unique=True)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_fuelcodestatus_CREATE_USER', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_fuelcodestatus_UPDATE_USER', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fuel_code_status',
            },
            bases=(models.Model, db_comments.model_mixins.DBComments),
        ),
    ]