from django.conf.urls import *
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from .views import PhotoListView, PhotoDetailView, TravelogueListView, \
    TravelogueDetailView, PhotoArchiveIndexView, PhotoDateDetailView, PhotoDayArchiveView, \
    PhotoYearArchiveView, PhotoMonthArchiveView, TravelogueArchiveIndexView, TravelogueYearArchiveView, \
    TravelogueDateDetailView, TravelogueDayArchiveView, TravelogueMonthArchiveView, TravelogueDateDetailOldView, \
    TravelogueDayArchiveOldView, TravelogueMonthArchiveOldView, PhotoDateDetailOldView, \
    PhotoDayArchiveOldView, PhotoMonthArchiveOldView

"""NOTE: the url names are changing. In the long term, I want to remove the 'pl-'
prefix on all urls, and instead rely on an application namespace 'Travelogue'.

At the same time, I want to change some URL patterns, e.g. for pagination. Changing the urls
twice within a few releases, could be confusing, so instead I am updating URLs bit by bit.

The new style will coexist with the existing 'pl-' prefix for a couple of releases.

"""


urlpatterns = patterns('',

                       url(r'^travelogue/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
                           TravelogueDateDetailView.as_view(month_format='%m'),
                           name='travelogue-detail'),
                       url(r'^travelogue/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
                           TravelogueDayArchiveView.as_view(month_format='%m'),
                           name='travelogue-archive-day'),
                       url(r'^travelogue/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
                           TravelogueMonthArchiveView.as_view(month_format='%m'),
                           name='travelogue-archive-month'),
                       url(r'^travelogue/(?P<year>\d{4})/$',
                           TravelogueYearArchiveView.as_view(),
                           name='pl-travelogue-archive-year'),
                       url(r'^travelogue/$',
                           TravelogueArchiveIndexView.as_view(),
                           name='pl-travelogue-archive'),
                       url(r'^$',
                           RedirectView.as_view(url=reverse_lazy('travelogue:pl-travelogue-archive')),
                           name='pl-travelogue-root'),
                       url(r'^travelogue/(?P<slug>[\-\d\w]+)/$',
                           TravelogueDetailView.as_view(), name='pl-travelogue'),
                       url(r'^traveloguelist/$',
                           TravelogueListView.as_view(),
                           name='travelogue-list'),

                       url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
                           PhotoDateDetailView.as_view(month_format='%m'),
                           name='photo-detail'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
                           PhotoDayArchiveView.as_view(month_format='%m'),
                           name='photo-archive-day'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
                           PhotoMonthArchiveView.as_view(month_format='%m'),
                           name='photo-archive-month'),
                       url(r'^photo/(?P<year>\d{4})/$',
                           PhotoYearArchiveView.as_view(),
                           name='pl-photo-archive-year'),
                       url(r'^photo/$',
                           PhotoArchiveIndexView.as_view(),
                           name='pl-photo-archive'),

                       url(r'^photo/(?P<slug>[\-\d\w]+)/$',
                           PhotoDetailView.as_view(),
                           name='pl-photo'),
                       url(r'^photolist/$',
                           PhotoListView.as_view(),
                           name='photo-list'),

                       # Deprecated URLs.
                       url(r'^travelogue/page/(?P<page>[0-9]+)/$',
                           TravelogueListView.as_view(),
                           {'deprecated_pagination': True},
                           name='pl-travelogue-list'),
                       url(r'^photo/page/(?P<page>[0-9]+)/$',
                           PhotoListView.as_view(),
                           {'deprecated_pagination': True},
                           name='pl-photo-list'),

                       url(r'^travelogue/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
                           TravelogueDateDetailOldView.as_view(),
                           name='pl-travelogue-detail'),
                       url(r'^travelogue/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
                           TravelogueDayArchiveOldView.as_view(),
                           name='pl-travelogue-archive-day'),
                       url(r'^travelogue/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
                           TravelogueMonthArchiveOldView.as_view(),
                           name='pl-travelogue-archive-month'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
                           PhotoDateDetailOldView.as_view(),
                           name='pl-photo-detail'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
                           PhotoDayArchiveOldView.as_view(),
                           name='pl-photo-archive-day'),
                       url(r'^photo/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
                           PhotoMonthArchiveOldView.as_view(),
                           name='pl-photo-archive-month')
                       )
