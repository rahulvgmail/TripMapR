from django.conf import settings
from django.utils import unittest

from .helpers import TravelogueBaseTest
from .factories import TravelogueFactory
from ..sitemaps import TravelogueSitemap, PhotoSitemap


@unittest.skipUnless('django.contrib.sitemaps' in settings.INSTALLED_APPS,
                     'Sitemaps not installed in this project, nothing to test.')
class SitemapTest(TravelogueBaseTest):

    urls = 'travelogue.tests.test_urls'

    def test_get_photo(self):
        """Default test setup contains one photo, this should appear in the sitemap."""
        response = self.client.get('/sitemap.xml')
        self.assertContains(response,
                            '<url><loc>http://tripmapr.com/ptests/photo/landscape/</loc>'
                            '<lastmod>2011-12-23</lastmod></url>')

    def test_get_travelogue(self):
        """if we add a travelogue to the site, we should see both the travelogue and
        the photo in the sitemap."""
        self.travelogue = TravelogueFactory(slug='test-travelogue')

        response = self.client.get('/sitemap.xml')
        self.assertContains(response,
                            '<url><loc>http://tripmapr.com/ptests/photo/landscape/</loc>'
                            '<lastmod>2011-12-23</lastmod></url>')
        self.assertContains(response,
                            '<url><loc>http://tripmapr.com/ptests/travelogue/test-travelogue/</loc>'
                            '<lastmod>2011-12-23</lastmod></url>')
