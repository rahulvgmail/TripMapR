# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sortedm2m.fields
import django.core.validators
import django.utils.timezone
import travelogue.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_set_site_domain_and_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('image', models.ImageField(upload_to=travelogue.models.get_storage_path, verbose_name='image')),
                ('date_taken', models.DateTimeField(editable=False, null=True, verbose_name='date taken', blank=True)),
                ('view_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='view count')),
                ('crop_from', models.CharField(default='center', choices=[('top', 'Top'), ('right', 'Right'), ('bottom', 'Bottom'), ('left', 'Left'), ('center', 'Center (Default)')], max_length=10, verbose_name='crop from', blank=True)),
                ('title', models.CharField(max_length=60, verbose_name='title', unique=True)),
                ('slug', models.SlugField(help_text='A "slug" is a unique URL-friendly title for an object.', verbose_name='slug', unique=True)),
                ('caption', models.TextField(verbose_name='caption', blank=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added')),
                ('is_public', models.BooleanField(default=True, help_text='Public photographs will be displayed in the default views.', verbose_name='is public')),
                ('tags', travelogue.models.TagField(help_text='Django-tagging was not found, tags will be treated as plain text.', max_length=255, verbose_name='tags', blank=True)),
            ],
            options={
                'verbose_name_plural': 'photos',
                'get_latest_by': 'date_added',
                'ordering': ['-date_added'],
                'verbose_name': 'photo',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoEffect',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name', unique=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('transpose_method', models.CharField(choices=[('FLIP_LEFT_RIGHT', 'Flip left to right'), ('FLIP_TOP_BOTTOM', 'Flip top to bottom'), ('ROTATE_90', 'Rotate 90 degrees counter-clockwise'), ('ROTATE_270', 'Rotate 90 degrees clockwise'), ('ROTATE_180', 'Rotate 180 degrees')], max_length=15, verbose_name='rotate or flip', blank=True)),
                ('color', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a black and white image, a factor of 1.0 gives the original image.', verbose_name='color')),
                ('brightness', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a black image, a factor of 1.0 gives the original image.', verbose_name='brightness')),
                ('contrast', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a solid grey image, a factor of 1.0 gives the original image.', verbose_name='contrast')),
                ('sharpness', models.FloatField(default=1.0, help_text='A factor of 0.0 gives a blurred image, a factor of 1.0 gives the original image.', verbose_name='sharpness')),
                ('filters', models.CharField(help_text='Chain multiple filters using the following pattern "FILTER_ONE->FILTER_TWO->FILTER_THREE". Image filters will be applied in order. The following filters are available: BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE.', max_length=200, verbose_name='filters', blank=True)),
                ('reflection_size', models.FloatField(default=0, help_text='The height of the reflection as a percentage of the orignal image. A factor of 0.0 adds no reflection, a factor of 1.0 adds a reflection equal to the height of the orignal image.', verbose_name='size')),
                ('reflection_strength', models.FloatField(default=0.6, help_text='The initial opacity of the reflection gradient.', verbose_name='strength')),
                ('background_color', models.CharField(default='#FFFFFF', help_text='The background color of the reflection gradient. Set this to match the background color of your page.', max_length=7, verbose_name='color')),
            ],
            options={
                'verbose_name_plural': 'photo effects',
                'verbose_name': 'photo effect',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhotoSize',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(help_text='Photo size name should contain only letters, numbers and underscores. Examples: "thumbnail", "display", "small", "main_page_widget".', validators=[django.core.validators.RegexValidator(message='Use only plain lowercase letters (ASCII), numbers and underscores.', regex='^[a-z0-9_]+$')], max_length=40, verbose_name='name', unique=True)),
                ('width', models.PositiveIntegerField(default=0, help_text='If width is set to "0" the image will be scaled to the supplied height.', verbose_name='width')),
                ('height', models.PositiveIntegerField(default=0, help_text='If height is set to "0" the image will be scaled to the supplied width', verbose_name='height')),
                ('quality', models.PositiveIntegerField(default=70, help_text='JPEG image quality.', choices=[(30, 'Very Low'), (40, 'Low'), (50, 'Medium-Low'), (60, 'Medium'), (70, 'Medium-High'), (80, 'High')], verbose_name='quality')),
                ('upscale', models.BooleanField(default=False, help_text='If selected the image will be scaled up if necessary to fit the supplied dimensions. Cropped sizes will be upscaled regardless of this setting.', verbose_name='upscale images?')),
                ('crop', models.BooleanField(default=False, help_text='If selected the image will be scaled and cropped to fit the supplied dimensions.', verbose_name='crop to fit?')),
                ('pre_cache', models.BooleanField(default=False, help_text='If selected this photo size will be pre-cached as photos are added.', verbose_name='pre-cache?')),
                ('increment_count', models.BooleanField(default=False, help_text='If selected the image\'s "view_count" will be incremented when this photo size is displayed.', verbose_name='increment view count?')),
                ('effect', models.ForeignKey(blank=True, to='travelogue.PhotoEffect', related_name='photo_sizes', null=True, verbose_name='photo effect')),
            ],
            options={
                'verbose_name_plural': 'photo sizes',
                'ordering': ['width', 'height'],
                'verbose_name': 'photo size',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Travelogue',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('title', models.CharField(max_length=50, verbose_name='title', unique=True)),
                ('slug', models.SlugField(help_text='A "slug" is a unique URL-friendly title for an object.', verbose_name='title slug', unique=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('is_public', models.BooleanField(default=True, help_text='Public Travelogues will be displayed in the default views.', verbose_name='is public')),
                ('tags', travelogue.models.TagField(help_text='Django-tagging was not found, tags will be treated as plain text.', max_length=255, verbose_name='tags', blank=True)),
                ('photos', sortedm2m.fields.SortedManyToManyField(help_text=None, verbose_name='photos', to='travelogue.Photo', blank=True, null=True, related_name='Travelogues')),
                ('sites', models.ManyToManyField(null=True, verbose_name='sites', blank=True, to='sites.Site')),
            ],
            options={
                'verbose_name_plural': 'Travelogues',
                'get_latest_by': 'date_added',
                'ordering': ['-date_added'],
                'verbose_name': 'Travelogue',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Watermark',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name', unique=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('image', models.ImageField(upload_to='Travelogue/watermarks', verbose_name='image')),
                ('style', models.CharField(default='scale', choices=[('tile', 'Tile'), ('scale', 'Scale')], max_length=5, verbose_name='style')),
                ('opacity', models.FloatField(default=1, help_text='The opacity of the overlay.', verbose_name='opacity')),
            ],
            options={
                'verbose_name_plural': 'watermarks',
                'verbose_name': 'watermark',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='photosize',
            name='watermark',
            field=models.ForeignKey(blank=True, to='travelogue.Watermark', related_name='photo_sizes', null=True, verbose_name='watermark image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='effect',
            field=models.ForeignKey(blank=True, to='travelogue.PhotoEffect', related_name='photo_related', null=True, verbose_name='effect'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='sites',
            field=models.ManyToManyField(null=True, verbose_name='sites', blank=True, to='sites.Site'),
            preserve_default=True,
        ),
    ]
