# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.core.files.storage import default_storage
from ..models import Image, Photo, TRAVELOGUE_DIR, TRAVELOGUE_CACHEDIRTAG
from .factories import LANDSCAPE_IMAGE_PATH, QUOTING_IMAGE_PATH, \
    TravelogueFactory, PhotoFactory
from .helpers import TravelogueBaseTest


class PhotoTest(TravelogueBaseTest):

    def tearDown(self):
        """Delete any extra test files (if created)."""
        super(PhotoTest, self).tearDown()
        try:
            self.pl2.delete()
        except:
            pass

    def test_new_photo(self):
        self.assertEqual(Photo.objects.count(), 1)
        self.assertTrue(self.pl.image.storage.exists(self.pl.image.name))
        self.assertEqual(self.pl.image.storage.size(self.pl.image.name),
                         os.path.getsize(LANDSCAPE_IMAGE_PATH))

    # def test_exif(self):
    #    self.assertTrue(len(self.pl.EXIF.keys()) > 0)

    def test_paths(self):
        self.assertEqual(os.path.normpath(str(self.pl.cache_path())).lower(),
                         os.path.normpath(os.path.join(TRAVELOGUE_DIR,
                                                       'photos',
                                                       'cache')).lower())
        self.assertEqual(self.pl.cache_url(),
                         settings.MEDIA_URL + TRAVELOGUE_DIR + '/photos/cache')

    def test_cachedir_tag(self):
        self.assertTrue(default_storage.exists(TRAVELOGUE_CACHEDIRTAG))

        content = default_storage.open(TRAVELOGUE_CACHEDIRTAG).read()
        self.assertEqual(content, b"Signature: 8a477f597d28d172789f06886806bc55")

    def test_count(self):
        for i in range(5):
            self.pl.get_testPhotoSize_url()
        self.assertEqual(self.pl.view_count, 0)
        self.s.increment_count = True
        self.s.save()
        for i in range(5):
            self.pl.get_testPhotoSize_url()
        self.assertEqual(self.pl.view_count, 5)

    def test_precache(self):
        # set the thumbnail photo size to pre-cache
        self.s.pre_cache = True
        self.s.save()
        # make sure it created the file
        self.assertTrue(self.pl.image.storage.exists(
            self.pl.get_testPhotoSize_filename()))
        self.s.pre_cache = False
        self.s.save()
        # clear the cache and make sure the file's deleted
        self.pl.clear_cache()
        self.assertFalse(self.pl.image.storage.exists(
            self.pl.get_testPhotoSize_filename()))

    def test_accessor_methods(self):
        self.assertEqual(self.pl.get_testPhotoSize_photosize(), self.s)
        self.assertEqual(self.pl.get_testPhotoSize_size(),
                         Image.open(self.pl.image.storage.open(
                             self.pl.get_testPhotoSize_filename())).size)
        self.assertEqual(self.pl.get_testPhotoSize_url(),
                         self.pl.cache_url() + '/' +
                         self.pl._get_filename_for_size(self.s))
        self.assertEqual(self.pl.get_testPhotoSize_filename(),
                         os.path.join(self.pl.cache_path(),
                                      self.pl._get_filename_for_size(self.s)))

    def test_quoted_url(self):
        """Test for issue #29 - filenames of photos are incorrectly quoted when
        building a URL."""

        # Check that a 'normal' path works ok.
        self.assertEqual(self.pl.get_testPhotoSize_url(),
                         self.pl.cache_url() + '/test_photologue_landscape_testPhotoSize.jpg')

        # Now create a Photo with a name that needs quoting.
        self.pl2 = PhotoFactory(image__from_path=QUOTING_IMAGE_PATH)
        self.assertEqual(self.pl2.get_testPhotoSize_url(),
                         self.pl2.cache_url() + '/test_photologue_%26quoting_testPhotoSize.jpg')

    def test_unicode(self):
        """Trivial check that unicode titles work.
        (I was trying to track down an elusive unicode issue elsewhere)"""
        PhotoFactory(title='É', 
            slug='é')

class PhotoManagerTest(TravelogueBaseTest):

    """Some tests for the methods on the Photo manager class."""

    def setUp(self):
        """Create 2 photos."""
        super(PhotoManagerTest, self).setUp()
        self.pl2 = PhotoFactory()

    def tearDown(self):
        super(PhotoManagerTest, self).tearDown()
        self.pl2.delete()

    def test_public(self):
        """Method 'is_public' should only return photos flagged as public."""
        self.assertEqual(Photo.objects.is_public().count(), 2)
        self.pl.is_public = False
        self.pl.save()
        self.assertEqual(Photo.objects.is_public().count(), 1)


class PreviousNextTest(TravelogueBaseTest):

    """Tests for the methods that provide the previous/next photos in a travelogue."""

    def setUp(self):
        """Create a test travelogue with 2 photos."""
        super(PreviousNextTest, self).setUp()
        self.test_travelogue = TravelogueFactory()
        self.pl1 = PhotoFactory()
        self.pl2 = PhotoFactory()
        self.pl3 = PhotoFactory()
        self.test_travelogue.photos.add(self.pl1)
        self.test_travelogue.photos.add(self.pl2)
        self.test_travelogue.photos.add(self.pl3)

    def tearDown(self):
        super(PreviousNextTest, self).tearDown()
        self.pl1.delete()
        self.pl2.delete()
        self.pl3.delete()

    def test_previous_simple(self):
        # Previous in travelogue.
        self.assertEqual(self.pl1.get_previous_in_travelogue(self.test_travelogue),
                         None)
        self.assertEqual(self.pl2.get_previous_in_travelogue(self.test_travelogue),
                         self.pl1)
        self.assertEqual(self.pl3.get_previous_in_travelogue(self.test_travelogue),
                         self.pl2)

    def test_previous_public(self):
        """What happens if one of the photos is not public."""
        self.pl2.is_public = False
        self.pl2.save()

        self.assertEqual(self.pl1.get_previous_in_travelogue(self.test_travelogue),
                         None)
        self.assertRaisesMessage(ValueError,
                                 'Cannot determine neighbours of a non-public photo.',
                                 self.pl2.get_previous_in_travelogue,
                                 self.test_travelogue)
        self.assertEqual(self.pl3.get_previous_in_travelogue(self.test_travelogue),
                         self.pl1)

    def test_previous_travelogue_mismatch(self):
        """Photo does not belong to the travelogue."""
        self.pl4 = PhotoFactory()

        self.assertRaisesMessage(ValueError,
                                 'Photo does not belong to travelogue.',
                                 self.pl4.get_previous_in_travelogue,
                                 self.test_travelogue)

        self.pl4.delete()

    def test_next_simple(self):
        # Next in travelogue.
        self.assertEqual(self.pl1.get_next_in_travelogue(self.test_travelogue),
                         self.pl2)
        self.assertEqual(self.pl2.get_next_in_travelogue(self.test_travelogue),
                         self.pl3)
        self.assertEqual(self.pl3.get_next_in_travelogue(self.test_travelogue),
                         None)

    def test_next_public(self):
        """What happens if one of the photos is not public."""
        self.pl2.is_public = False
        self.pl2.save()

        self.assertEqual(self.pl1.get_next_in_travelogue(self.test_travelogue),
                         self.pl3)
        self.assertRaisesMessage(ValueError,
                                 'Cannot determine neighbours of a non-public photo.',
                                 self.pl2.get_next_in_travelogue,
                                 self.test_travelogue)
        self.assertEqual(self.pl3.get_next_in_travelogue(self.test_travelogue),
                         None)

    def test_next_travelogue_mismatch(self):
        """Photo does not belong to the travelogue."""
        self.pl4 = PhotoFactory()

        self.assertRaisesMessage(ValueError,
                                 'Photo does not belong to travelogue.',
                                 self.pl4.get_next_in_travelogue,
                                 self.test_travelogue)

        self.pl4.delete()
