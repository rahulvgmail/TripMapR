from .. import models
from .helpers import TravelogueBaseTest
from .factories import TravelogueFactory, PhotoFactory, TripNoteFactory, TrailPointFactory
from django.contrib.gis.geos import Point

class TravelogueTest(TravelogueBaseTest):

    def setUp(self):
        """Create a test travelogue with 2 photos."""
        super(TravelogueTest, self).setUp()
        self.test_travelogue =TravelogueFactory()
        self.pl2 = PhotoFactory()
        self.tpoint = TrailPointFactory(point = Point(22.4604, 33.9420, 0.0))
        self.tnf2 = TripNoteFactory()
        self.tnf2.location_detail = self.tpoint
        self.test_travelogue.photos.add(self.pl)
        self.test_travelogue.photos.add(self.pl2)
        self.test_travelogue.notes.add(self.tnf)
        self.test_travelogue.notes.add(self.tnf2)

    def tearDown(self):
        super(TravelogueTest, self).tearDown()
        self.pl2.delete()

    def test_public(self):
        """Method 'public' should only return photos flagged as public."""
        self.assertEqual(self.test_travelogue.public().count(), 2)
        self.pl.is_public = False
        self.pl.save()
        self.assertEqual(self.test_travelogue.public().count(), 1)

    def test_photo_count(self):
        """Method 'photo_count' should return the count of the photos in this
        travelogue."""
        self.assertEqual(self.test_travelogue.photo_count(), 2)
        self.pl.is_public = False
        self.pl.save()
        self.assertEqual(self.test_travelogue.photo_count(), 1)

        # Method takes an optional 'public' kwarg.
        self.assertEqual(self.test_travelogue.photo_count(public=False), 2)

    def test_sample(self):
        """Method 'sample' should return a random queryset of photos from the
        travelogue."""

        # By default we return all photos from the travelogue (but ordered at random).
        _current_sample_size = models.SAMPLE_SIZE
        models.SAMPLE_SIZE = 5
        self.assertEqual(len(self.test_travelogue.sample()), 2)

        # We can state how many photos we want.
        self.assertEqual(len(self.test_travelogue.sample(count=1)), 1)

        # If only one photo is public then the sample cannot have more than one
        # photo.
        self.pl.is_public = False
        self.pl.save()
        self.assertEqual(len(self.test_travelogue.sample(count=2)), 1)

        self.pl.is_public = True
        self.pl.save()

        # We can limit the number of photos by changing settings.
        models.SAMPLE_SIZE = 1
        self.assertEqual(len(self.test_travelogue.sample()), 1)

        models.SAMPLE_SIZE = _current_sample_size
