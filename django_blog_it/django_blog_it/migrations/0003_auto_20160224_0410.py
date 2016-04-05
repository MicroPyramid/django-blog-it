# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_blog_it', '0002_auto_20160223_0521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(default=b'Drafted', max_length=10, choices=[(b'Drafted', b'Drafted'), (b'Published', b'Published'), (b'Rejected', b'Rejected'), (b'Trashed', b'Trashed')]),
        ),
    ]
