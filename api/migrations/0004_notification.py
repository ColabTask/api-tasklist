# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-23 00:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_task_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.DateField(verbose_name='Published date')),
                ('modification_date', models.DateField(blank=True, null=True, verbose_name='Modification Date')),
                ('status', models.IntegerField(default=1, verbose_name='Status')),
                ('target_type', models.CharField(max_length=50, verbose_name='Target type')),
                ('target_id', models.PositiveIntegerField(verbose_name='Target ID')),
                ('target_intention', models.CharField(max_length=50, verbose_name='Target intention')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('text', models.TextField(verbose_name='Text')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_received', to=settings.AUTH_USER_MODEL, verbose_name='Receiver')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_sent', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
            options={
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
