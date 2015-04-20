from django.conf.urls import *
from ..sitemaps import TravelogueSitemap, PhotoSitemap


urlpatterns = patterns('',
              url(r'^travelogue/', include('travelogue.urls', namespace='travelogue')),
)

sitemaps = {'travelogue_travelogues': TravelogueSitemap,
            'travelogue_photos': PhotoSitemap,
            }

urlpatterns += patterns('',
                        (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps':
                                                                                     sitemaps})
                        )
