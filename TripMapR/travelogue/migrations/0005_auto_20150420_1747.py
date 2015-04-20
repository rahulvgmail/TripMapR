# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travelogue', '0004_auto_20150418_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripnote',
            name='date_taken',
            field=models.DateTimeField(verbose_name='date note captured by user on the field', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tripnote',
            name='view_count',
            field=models.PositiveIntegerField(default=0, verbose_name='view count', editable=False),
            preserve_default=True,
        ),
    ]
