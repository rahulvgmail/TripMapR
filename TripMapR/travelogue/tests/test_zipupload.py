import copy

from django.test import TestCase
from users.models import User

from ..models import Travelogue, Photo
from .factories import TravelogueFactory, PhotoFactory, SAMPLE_ZIP_PATH, SAMPLE_NOT_IMAGE_ZIP_PATH, \
    IGNORED_FILES_ZIP_PATH, LANDSCAPE_IMAGE_PATH


class TravelogueUploadTest(TestCase):

    """Testing the admin page that allows users to upload zips."""

    def setUp(self):
        super(TravelogueUploadTest, self).setUp()
      #  user = User(username = 'etah', first_name = "rahul", last_name= "verma", 
      #                     email = "rahulv@gmail.com", password = "secret")
        user = User.objects.create_user(username = 'etah', email='rahulv@gmail.com', password='secret')
        user.is_staff = True
        user.save()
        self.assertTrue(self.client.login(username='etah', password='secret'))

        self.zip_file = open(SAMPLE_ZIP_PATH, mode='rb')

        self.sample_form_data = {'zip_file': self.zip_file,
                                 'title': 'This is a test title'}

    def tearDown(self):
        super(TravelogueUploadTest, self).tearDown()
        self.zip_file.close()
        for photo in Photo.objects.all():
            photo.delete()

    def test_get(self):
        """We can get the custom admin page."""

        response = self.client.get('/admin/travelogue/photo/upload_zip/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/travelogue/photo/upload_zip.html')

        self.assertContains(response, 'Upload a zip archive of photos')

    def test_breadcrumbs(self):
        """Quick check that the breadcrumbs are generated correctly."""

        response = self.client.get('/admin/travelogue/photo/upload_zip/')
        self.assertContains(
            response, """<div class="breadcrumbs"><a href="/admin/">Home</a> &rsaquo;
            <a href="/admin/travelogue/">Travelogue</a> &rsaquo; Photos &rsaquo; Upload </div>""", html=True)

    def test_missing_fields(self):
        """Missing fields mean the form is redisplayed with errors."""

        test_data = copy.copy(self.sample_form_data)
        del test_data['zip_file']
        response = self.client.post('/admin/travelogue/photo/upload_zip/', test_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_good_data(self):
        """Upload a zip with a single file it it: 'sample.jpg'.
        It gets assigned to a newly created travelogue 'Test'."""

        test_data = copy.copy(self.sample_form_data)
        response = self.client.post('/admin/travelogue/photo/upload_zip/', test_data)
        self.assertEqual(response['Location'],
                         'http://testserver/admin/travelogue/photo/')

        self.assertQuerysetEqual(Travelogue.objects.all(),
                                 ['<Travelogue: This is a test title>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: This is a test title 1>'])

        # The photo is attached to the travelogue.
        travelogue = Travelogue.objects.get(title='This is a test title')
        self.assertQuerysetEqual(travelogue.photos.all(),
                                 ['<Photo: This is a test title 1>'])

    def test_duplicate_travelogue(self):
        """If we try to create a Travelogue with a title that duplicates an existing title, refuse to load."""

        TravelogueFactory(title='This is a test title')

        test_data = copy.copy(self.sample_form_data)
        response = self.client.post('/admin/travelogue/photo/upload_zip/', test_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form']['title'].errors)

    def test_title_or_travelogue(self):
        """We should supply either a title field or a travelogue."""

        test_data = copy.copy(self.sample_form_data)
        del test_data['title']
        response = self.client.post('/admin/travelogue/photo/upload_zip/', test_data)
        self.assertEqual(list(response.context['form'].non_field_errors()),
                         ['Select an existing travelogue, or enter a title for a new travelogue.'])

    def test_not_image(self):
        """A zip with a file of the wrong format (.txt).
        That file gets ignored."""

        test_data = copy.copy(self.sample_form_data)
        with open(SAMPLE_NOT_IMAGE_ZIP_PATH, mode='rb') as f:
            test_data['zip_file'] = f
            response = self.client.post('/admin/travelogue/photo/upload_zip/', test_data)
            self.assertEqual(response.status_code, 302)

        self.assertQuerysetEqual(Travelogue.objects.all(),
                                 ['<Travelogue: This is a test title>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: This is a test title 1>'])

    def test_ignored(self):
        """Ignore anything that does not look like a image file.
        E.g. hidden files, and folders.
        We have two images: one in the top level of the zip, and one in a subfolder.
        The second one gets ignored - we only process files at the zip root."""

        test_data = copy.copy(self.sample_form_data)
        with open(IGNORED_FILES_ZIP_PATH, mode='rb') as f:
            test_data['zip_file'] = f
            response = self.client.post('/admin/travelogue/photo/upload_zip/', test_data)
            self.assertEqual(response.status_code, 302)

        self.assertQuerysetEqual(Travelogue.objects.all(),
                                 ['<Travelogue: This is a test title>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: This is a test title 1>'])

    def test_existing(self):
        """Add the photos in the zip to an existing travelogue."""

        existing = TravelogueFactory(title='Existing')

        test_data = copy.copy(self.sample_form_data)
        test_data['travelogue'] = existing.id
        response = self.client.post('/admin/travelogue/photo/upload_zip/', test_data)
        self.assertEqual(response.status_code, 302)

        self.assertQuerysetEqual(Travelogue.objects.all(),
                                 ['<Travelogue: Existing>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: Existing 1>'])

        # The photo is attached to the existing travelogue.
        self.assertQuerysetEqual(existing.photos.all(),
                                 ['<Photo: Existing 1>'])

    def test_duplicate_title(self):
        """If we try to create a Photo from the archive with a title
        that duplicates an existing title, raise a warning."""

        photo = PhotoFactory(title='Test 1')

        test_data = copy.copy(self.sample_form_data)
        test_data['title'] = 'Test'
        response = self.client.post('/admin/travelogue/photo/upload_zip/', test_data)
        self.assertEqual(response.status_code, 302)

        self.assertQuerysetEqual(Travelogue.objects.all(),
                                 ['<Travelogue: Test>'])
        self.assertQuerysetEqual(Photo.objects.all(),
                                 ['<Photo: Test 1>'])

        # The (existing) photo is NOT attached to the travelogue.
        travelogue = Travelogue.objects.get(title='Test')
        self.assertQuerysetEqual(travelogue.photos.all(),
                                 [])

        # And a warning message is sent to the user - we reload the page to see it.
        response = self.client.get('/admin/travelogue/photo/upload_zip/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            """<li class="warning">Did not create photo &quot;%(filename)s&quot; with slug
                            &quot;test-1&quot; as a photo with that slug already exists.</li>""",
                            html=True)

        # Housekeeping.
        photo.delete()

    def test_bad_zip(self):
        """Supplied file is not a zip file - tell user."""

        test_data = copy.copy(self.sample_form_data)
        with open(LANDSCAPE_IMAGE_PATH, mode='rb') as f:
            test_data['zip_file'] = f
            response = self.client.post('/admin/travelogue/photo/upload_zip/', test_data)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form']['zip_file'].errors)
