# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-22 06:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_blog_it', '0011_auto_20160719_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Google',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_id', models.CharField(default='', max_length=200)),
                ('google_url', models.CharField(default='', max_length=1000)),
                ('verified_email', models.CharField(default='', max_length=200)),
                ('family_name', models.CharField(default='', max_length=200)),
                ('name', models.CharField(default='', max_length=200)),
                ('picture', models.CharField(default='', max_length=200)),
                ('gender', models.CharField(default='', max_length=10)),
                ('dob', models.CharField(default='', max_length=50)),
                ('given_name', models.CharField(default='', max_length=200)),
                ('email', models.CharField(db_index=True, default='', max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='google', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='featured_image',
            field=models.ImageField(blank=True, null=True, upload_to='static/blog/uploads/%Y/%m/%d/'),
        ),
    ]
