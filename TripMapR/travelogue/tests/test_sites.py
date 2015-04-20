from django.test import TestCase
from django.contrib.sites.models import Site
from django.utils import unittest
from django.conf import settings

from .factories import TravelogueFactory, PhotoFactory


class SitesTest(TestCase):

    urls = 'travelogue.tests.test_urls'

    def setUp(self):
        """
        Create two example sites that we can use to test what gets displayed
        where.
        """
        super(SitesTest, self).setUp()

        max_id = Site.objects.latest('id').id
        self.site1 = Site.objects.get(pk= max_id)
        self.site2 = Site.objects.get(pk= max_id)

     #   print max_id
        try:
            self.site1, created1 = Site.objects.get_or_create(
                domain="tripmapr.com", name="tripmapr.com")
            self.site2, created2 = Site.objects.get_or_create(
                 domain="tripmapr.org", name="tripmapr.org")
        except:
            pass

        
 
        with self.settings(PHOTOLOGUE_MULTISITE=True):
            # Be explicit about linking Galleries/Photos to Sites."""
            self.travelogue1 = TravelogueFactory(slug='test-travelogue', sites=[self.site1])
            self.travelogue2 = TravelogueFactory(slug='not-on-site-travelogue')
            self.photo1 = PhotoFactory(slug='test-photo', sites=[self.site1])
            self.photo2 = PhotoFactory(slug='not-on-site-photo')
            self.travelogue1.photos.add(self.photo1, self.photo2)

        # I'd like to use factory_boy's mute_signal decorator but that
        # will only available once factory_boy 2.4 is released. So long
        # we'll have to remove the site association manually
        self.photo2.sites.clear()

    def tearDown(self):
        super(SitesTest, self).tearDown()
        self.travelogue1.delete()
        self.travelogue2.delete()
        self.photo1.delete()
        self.photo2.delete()

    def test_basics(self):
        """ See if objects were added automatically (by the factory) to the current site. """
        self.assertEqual(list(self.travelogue1.sites.all()), [self.site1])
        self.assertEqual(list(self.photo1.sites.all()), [self.site1])

    def test_auto_add_sites(self):
        """
        Objects should not be automatically associated with a particular site when
        ``PHOTOLOGUE_MULTISITE`` is ``True``.
        """

        with self.settings(PHOTOLOGUE_MULTISITE=False):
            travelogue = TravelogueFactory()
            photo = PhotoFactory()
        self.assertEqual(list(travelogue.sites.all()), [self.site1])
        self.assertEqual(list(photo.sites.all()), [self.site1])

        photo.delete()

        with self.settings(PHOTOLOGUE_MULTISITE=True):
            travelogue = TravelogueFactory()
            photo = PhotoFactory()
        self.assertEqual(list(travelogue.sites.all()), [])
        self.assertEqual(list(photo.sites.all()), [])

        photo.delete()

    def test_travelogue_list(self):
        response = self.client.get('/travelogue/traveloguelist/')
        self.assertEqual(list(response.context['object_list']), [self.travelogue1])

#    def test_travelogue_detail(self):
#        response = self.client.get('/travelogue/travelogue/test-travelogue/')
 #       self.assertEqual(response.context['object'], self.travelogue1)

  #      response = self.client.get('/travelogue/travelogue/not-on-site-travelogue/')
   #     self.assertEqual(response.status_code, 404)

#    def test_photo_list(self):
#        response = self.client.get('/travelogue/photolist/')
 #       self.assertEqual(list(response.context['object_list']), [self.photo1])

 #   def test_photo_detail(self):
 #       response = self.client.get('/travelogue/photo/test-photo/')
 #       self.assertEqual(response.context['object'], self.photo1)

 #       response = self.client.get('/travelogue/photo/not-on-site-photo/')
 #       self.assertEqual(response.status_code, 404)

#    def test_photo_archive(self):
#        response = self.client.get('/travelogue/photo/')
#        self.assertEqual(list(response.context['object_list']), [self.photo1])

#    def test_photos_in_travelogue(self):
        """
        Only those photos are supposed to be shown in a travelogue that are
        also associated with the current site.
        """
#        response = self.client.get('/travelogue/travelogue/test-travelogue/')
#        self.assertEqual(list(response.context['object'].public()), [self.photo1])

    @unittest.skipUnless('django.contrib.sitemaps' in settings.INSTALLED_APPS,
                         'Sitemaps not installed in this project, nothing to test.')
    def test_sitemap(self):
        """A sitemap should only show objects associated with the current site."""
        response = self.client.get('/sitemap.xml')

        # Check photos.
        self.assertContains(response,
                            '<url><loc>http://tripmapr.com/travelogue/photo/test-photo/</loc>'
                            '<lastmod>2011-12-23</lastmod></url>')
        self.assertNotContains(response,
                               '<url><loc>http://tripmapr.com/travelogue/photo/not-on-site-photo/</loc>'
                               '<lastmod>2011-12-23</lastmod></url>')

        # Check galleries.
        self.assertContains(response,
                            '<url><loc>http://tripmapr.com/travelogue/travelogue/test-travelogue/</loc>'
                            '<lastmod>2011-12-23</lastmod></url>')
        self.assertNotContains(response,
                               '<url><loc>http://tripmapr.com/travelogue/travelogue/not-on-site-travelogue/</loc>'
                               '<lastmod>2011-12-23</lastmod></url>')

    def test_orphaned_photos(self):
        self.assertEqual(list(self.travelogue1.orphaned_photos()), [self.photo2])

        self.travelogue2.photos.add(self.photo2)
        self.assertEqual(list(self.travelogue1.orphaned_photos()), [self.photo2])

        self.travelogue1.sites.clear()
        self.assertEqual(list(self.travelogue1.orphaned_photos()), [self.photo1, self.photo2])

        self.photo1.sites.clear()
        self.photo2.sites.clear()
        self.assertEqual(list(self.travelogue1.orphaned_photos()), [self.photo1, self.photo2])
