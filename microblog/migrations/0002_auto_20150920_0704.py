# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microblog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(blank=True, max_length=2, choices=[(b'Drafted', b'Draft'), (b'Published', b'Published'), (b'Rejected', b'Rejected')]),
        ),
    ]
