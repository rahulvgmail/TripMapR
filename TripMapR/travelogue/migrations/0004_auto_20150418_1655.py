# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_set_site_domain_and_name'),
        ('travelogue', '0003_auto_20150411_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='geotrack',
            name='sites',
            field=models.ManyToManyField(to='sites.Site', null=True, blank=True, verbose_name='sites'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trail',
            name='sites',
            field=models.ManyToManyField(to='sites.Site', null=True, blank=True, verbose_name='sites'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trailpoint',
            name='sites',
            field=models.ManyToManyField(to='sites.Site', null=True, blank=True, verbose_name='sites'),
            preserve_default=True,
        ),
    ]
