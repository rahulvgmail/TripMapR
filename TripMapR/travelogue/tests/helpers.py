from django.test import TestCase
from .factories import PhotoFactory, PhotoSizeFactory, TripNoteFactory, TrailPointFactory
from django.contrib.gis.geos import Point

class TravelogueBaseTest(TestCase):
      
    def setUp(self):
        self.s = PhotoSizeFactory(name='testPhotoSize',
                                  width=100,
                                  height=100)
        self.pl = PhotoFactory(title='Landscape',
                               slug='landscape')
        self.tpoint = TrailPointFactory(point = Point(12.4604, 43.9420, 0.0))
        self.tnf = TripNoteFactory(title='random',
                               slug='random')
        self.tnf.location_detail = self.tpoint


    def tearDown(self):
        # Need to manually remove the files created during testing.
        self.pl.delete()
