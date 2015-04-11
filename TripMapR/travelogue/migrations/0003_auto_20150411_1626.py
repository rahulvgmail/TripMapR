# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sortedm2m.fields
import django.contrib.gis.db.models.fields
import travelogue.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_set_site_domain_and_name'),
        ('travelogue', '0002_photosize_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('track', django.contrib.gis.db.models.fields.MultiLineStringField(dim=3, srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trail',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('tags', travelogue.models.TagField(help_text='Django-tagging was not found, tags will be treated as plain text.', verbose_name='tags', max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrailPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('point', django.contrib.gis.db.models.fields.PointField(dim=3, srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TripNote',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date_added', models.DateTimeField(verbose_name='date published', default=django.utils.timezone.now)),
                ('title', models.CharField(unique=True, verbose_name='title', max_length=50)),
                ('story', models.TextField(help_text='user story content as html', verbose_name='userStroy')),
                ('slug', models.SlugField(help_text='A "slug" is a unique URL-friendly title for an object.', verbose_name='slug', unique=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('is_public', models.BooleanField(help_text='Public TripNotes will be displayed in the default views.', verbose_name='is public', default=True)),
                ('tags', travelogue.models.TagField(help_text='Django-tagging was not found, tags will be treated as plain text.', verbose_name='tags', max_length=255, blank=True)),
                ('location_detail', models.ForeignKey(verbose_name='location_detail', related_name='tripnote_related', null=True, to='travelogue.TrailPoint', blank=True)),
                ('sites', models.ManyToManyField(verbose_name='sites', null=True, to='sites.Site', blank=True)),
            ],
            options={
                'verbose_name_plural': 'tripnotes',
                'get_latest_by': 'date_added',
                'verbose_name': 'tripnote',
                'ordering': ['-date_added'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='trail',
            name='geoPoints',
            field=models.ManyToManyField(verbose_name='geoPoints', null=True, to='travelogue.TrailPoint', blank=True),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='travelogue',
            options={'verbose_name_plural': 'travelogues', 'get_latest_by': 'date_added', 'verbose_name': 'travelogue', 'ordering': ['-date_added']},
        ),
        migrations.AddField(
            model_name='photo',
            name='location_detail',
            field=models.ForeignKey(verbose_name='location_detail', related_name='photo_related', null=True, to='travelogue.TrailPoint', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='travelogue',
            name='geoTrail',
            field=models.ForeignKey(verbose_name='geoTrail', related_name='travelogue_related', null=True, to='travelogue.Trail', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='travelogue',
            name='notes',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, verbose_name='tripNote', related_name='travelogues', null=True, to='travelogue.TripNote', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photosize',
            name='quality',
            field=models.PositiveIntegerField(help_text='JPEG image quality.', verbose_name='quality', default=70, choices=[(30, 'Very Low'), (40, 'Low'), (50, 'Medium-Low'), (60, 'Medium'), (70, 'Medium-High'), (80, 'High'), (90, 'Very High')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='travelogue',
            name='photos',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, verbose_name='photos', related_name='travelogues', null=True, to='travelogue.Photo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='watermark',
            name='image',
            field=models.ImageField(verbose_name='image', upload_to='travelogue/watermarks'),
            preserve_default=True,
        ),
    ]
