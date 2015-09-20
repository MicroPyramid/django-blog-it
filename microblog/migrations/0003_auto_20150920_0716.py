# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microblog', '0002_auto_20150920_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(blank=True, max_length=2, choices=[(b'D', b'Draft'), (b'P', b'Published'), (b'T', b'Rejected')]),
        ),
    ]
