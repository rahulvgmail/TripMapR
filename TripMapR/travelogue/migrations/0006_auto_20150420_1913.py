# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travelogue', '0005_auto_20150420_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripnote',
            name='date_taken',
            field=models.DateTimeField(null=True, verbose_name='date note captured by user on the field', blank=True),
            preserve_default=True,
        ),
    ]
