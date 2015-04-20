from django.test import TestCase
from .factories import TravelogueFactory


class RequestTravelogueTest(TestCase):

    urls = 'travelogue.tests.test_urls'

    def setUp(self):
        super(RequestTravelogueTest, self).setUp()
        self.travelogue = TravelogueFactory(slug='test-travelogue')

    def test_archive_travelogue_url_works(self):
        response = self.client.get('/travelogue/travelogue/')
        self.assertEqual(response.status_code, 200)

    def test_archive_travelogue_empty(self):
        """If there are no galleries to show, tell the visitor - don't show a
        404."""

        self.travelogue.is_public = False
        self.travelogue.save()

        response = self.client.get('/travelogue/travelogue/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['latest'].count(),
                         0)

    def test_paginated_travelogue_url_works(self):
        response = self.client.get('/travelogue/traveloguelist/')
        self.assertEqual(response.status_code, 200)

    def test_travelogue_works(self):
        response = self.client.get('/travelogue/travelogue/test-travelogue/')
        self.assertEqual(response.status_code, 200)

    def test_archive_year_travelogue_works(self):
        response = self.client.get('/travelogue/travelogue/2011/')
        self.assertEqual(response.status_code, 200)

    def test_archive_month_travelogue_works(self):
        response = self.client.get('/travelogue/travelogue/2011/12/')
        self.assertEqual(response.status_code, 200)

    def test_archive_day_travelogue_works(self):
        response = self.client.get('/travelogue/travelogue/2011/12/23/')
        self.assertEqual(response.status_code, 200)

    def test_detail_travelogue_works(self):
        response = self.client.get('/travelogue/travelogue/2011/12/23/test-travelogue/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_list(self):
        """Trivial test - if someone requests the root url of the app
        (i.e. /travelogue/'), redirect them to the travelogue list page."""
        response = self.client.get('/travelogue/')
        self.assertRedirects(response, '/travelogue/travelogue/', 301, 200)


class TraveloguePaginationTest(TestCase):

    urls = 'travelogue.tests.test_urls'

    def test_pagination(self):
        for i in range(1, 23):
            TravelogueFactory(title='travelogue{0:0>3}'.format(i))

        response = self.client.get('/travelogue/traveloguelist/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']),
                         20)
        # Check first and last items.
        self.assertEqual(response.context['object_list'][0].title,
                         'travelogue022')
        self.assertEqual(response.context['object_list'][19].title,
                         'travelogue003')

        # Now get the second page of results.
        response = self.client.get('/travelogue/traveloguelist/?page=2')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['object_list']),
                         2)
        # Check first and last items.
        self.assertEqual(response.context['object_list'][0].title,
                         'travelogue002')
        self.assertEqual(response.context['object_list'][1].title,
                         'travelogue001')
