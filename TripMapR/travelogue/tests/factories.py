import os
import datetime

from django.utils.text import slugify
from django.utils.timezone import utc
from django.utils import six
from django.conf import settings
from django.contrib.gis.geos import Point
try:
    import factory
except ImportError:
    raise ImportError(
        "No module named factory. To run travelogue's tests you need to install factory-boy.")

from ..models import Travelogue, ImageModel, Photo, PhotoSize, \
    Trail, TripNote, TrailPoint

RES_DIR = os.path.join(os.path.dirname(__file__), '../res')
LANDSCAPE_IMAGE_PATH = os.path.join(RES_DIR, 'test_photologue_landscape.jpg')
PORTRAIT_IMAGE_PATH = os.path.join(RES_DIR, 'test_photologue_portrait.jpg')
SQUARE_IMAGE_PATH = os.path.join(RES_DIR, 'test_photologue_square.jpg')
QUOTING_IMAGE_PATH = os.path.join(RES_DIR, 'test_photologue_&quoting.jpg')
SAMPLE_ZIP_PATH = os.path.join(RES_DIR, 'zips/sample.zip')
SAMPLE_NOT_IMAGE_ZIP_PATH = os.path.join(RES_DIR, 'zips/not_image.zip')
IGNORED_FILES_ZIP_PATH = os.path.join(RES_DIR, 'zips/ignored_files.zip')


class TravelogueFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Travelogue

    title = factory.Sequence(lambda n: 'travelogue{0:0>3}'.format(n))
    slug = factory.LazyAttribute(lambda a: slugify(six.text_type(a.title)))

    @factory.sequence
    def date_added(n):
        # Have to cater projects being non-timezone aware.
        if settings.USE_TZ:
            sample_date = datetime.datetime(
                year=2011, month=12, day=23, hour=17, minute=40, tzinfo=utc)
        else:
            sample_date = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40)
        return sample_date + datetime.timedelta(minutes=n)

    @factory.post_generation
    def sites(self, create, extracted, **kwargs):
        """
        Associates the object with the current site unless ``sites`` was passed,
        in which case the each item in ``sites`` is associated with the object.

        Note that if PHOTOLOGUE_MULTISITE is False, all Travelogue/Photos are automatically
        associated with the current site - bear this in mind when writing tests.
        """
        if not create:
            return
        if extracted:
            for site in extracted:
                self.sites.add(site)


class ImageModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ImageModel
        abstract = True


class PhotoFactory(ImageModelFactory):

    """Note: after creating Photo instances for tests, remember to manually
    delete them.
    """

    class Meta:
        model = Photo

    title = factory.Sequence(lambda n: 'photo{0:0>3}'.format(n))
    slug = factory.LazyAttribute(lambda a: slugify(six.text_type(a.title)))
    image = factory.django.ImageField(from_path=LANDSCAPE_IMAGE_PATH)

    @factory.sequence
    def date_added(n):
        # Have to cater projects being non-timezone aware.
        if settings.USE_TZ:
            sample_date = datetime.datetime(
                year=2011, month=12, day=23, hour=17, minute=40, tzinfo=utc)
        else:
            sample_date = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40)
        return sample_date + datetime.timedelta(minutes=n)

    @factory.post_generation
    def sites(self, create, extracted, **kwargs):
        """
        Associates the object with the current site unless ``sites`` was passed,
        in which case the each item in ``sites`` is associated with the object.

        Note that if PHOTOLOGUE_MULTISITE is False, all Travelogue/Photos are automatically
        associated with the current site - bear this in mind when writing tests.
        """
        if not create:
            return
        if extracted:
            for site in extracted:
                self.sites.add(site)

class TripNoteFactory(ImageModelFactory):

    """Note: after creating Photo instances for tests, remember to manually
    delete them.
    """

    class Meta:
        model = TripNote

    title = factory.Sequence(lambda n: 'tripnote{0:0>3}'.format(n))
    slug  = factory.LazyAttribute(lambda a: slugify(six.text_type(a.title)))
    story = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo 
           ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient
           montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, 
           sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, 
           vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. 
           Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus 
           elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor 
           eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, 
           feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. """


    @factory.sequence
    def date_added(n):
        # Have to cater projects being non-timezone aware.
        if settings.USE_TZ:
            sample_date = datetime.datetime(
                year=2011, month=12, day=23, hour=17, minute=40, tzinfo=utc)
        else:
            sample_date = datetime.datetime(year=2011, month=12, day=23, hour=17, minute=40)
        return sample_date + datetime.timedelta(minutes=n)

    @factory.post_generation
    def sites(self, create, extracted, **kwargs):
        """
        Associates the object with the current site unless ``sites`` was passed,
        in which case the each item in ``sites`` is associated with the object.

        Note that if PHOTOLOGUE_MULTISITE is False, all Travelogue/Photos are automatically
        associated with the current site - bear this in mind when writing tests.
        """
        if not create:
            return
        if extracted:
            for site in extracted:
                self.sites.add(site)


class PhotoSizeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = PhotoSize

    name = factory.Sequence(lambda n: 'name{0:0>3}'.format(n))


class TrailPointFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = TrailPoint

    point = Point(12.4604, 43.9420, 0.0)
    timestamp = datetime.datetime(
                year=2011, month=12, day=23, hour=17, minute=40, tzinfo=utc)   
