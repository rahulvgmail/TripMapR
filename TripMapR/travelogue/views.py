import warnings

from django.conf import settings
from django.views.generic.dates import ArchiveIndexView, DateDetailView, DayArchiveView, MonthArchiveView, \
    YearArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse

from .models import Photo, Travelogue

# Number of galleries to display per page.
GALLERY_PAGINATE_BY = getattr(settings, 'PHOTOLOGUE_GALLERY_PAGINATE_BY', 20)

if GALLERY_PAGINATE_BY != 20:
    warnings.warn(
        DeprecationWarning('PHOTOLOGUE_GALLERY_PAGINATE_BY setting will be removed in Photologue 3.2'))

# Number of photos to display per page.
PHOTO_PAGINATE_BY = getattr(settings, 'PHOTOLOGUE_PHOTO_PAGINATE_BY', 20)

if PHOTO_PAGINATE_BY != 20:
    warnings.warn(
        DeprecationWarning('PHOTOLOGUE_PHOTO_PAGINATE_BY setting will be removed in Photologue 3.2'))

# Travelogue views.


class TravelogueListView(ListView):
    queryset = Travelogue.objects.on_site().is_public()
    paginate_by = GALLERY_PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super(TravelogueListView, self).get_context_data(**kwargs)
        if self.kwargs.get('deprecated_pagination', False):
            warnings.warn(
                DeprecationWarning('Page numbers should now be passed via a page query-string parameter.'
                                   ' The old style "/page/n/"" will be removed in Photologue 3.2.'))
        return context


class TravelogueDetailView(DetailView):
    queryset = Travelogue.objects.on_site().is_public()


class TravelogueDateView(object):
    queryset = Travelogue.objects.on_site().is_public()
    date_field = 'date_added'
    allow_empty = True


class TravelogueDateDetailView(TravelogueDateView, DateDetailView):
    pass


class TravelogueArchiveIndexView(TravelogueDateView, ArchiveIndexView):
    pass


class TravelogueDayArchiveView(TravelogueDateView, DayArchiveView):
    pass


class TravelogueMonthArchiveView(TravelogueDateView, MonthArchiveView):
    pass


class TravelogueYearArchiveView(TravelogueDateView, YearArchiveView):
    make_object_list = True

# Photo views.


class PhotoListView(ListView):
    queryset = Photo.objects.on_site().is_public()
    paginate_by = PHOTO_PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super(PhotoListView, self).get_context_data(**kwargs)
        if self.kwargs.get('deprecated_pagination', False):
            warnings.warn(
                DeprecationWarning('Page numbers should now be passed via a page query-string parameter.'
                                   ' The old style "/page/n/"" will be removed in Photologue 3.2'))
        return context


class PhotoDetailView(DetailView):
    queryset = Photo.objects.on_site().is_public()


class PhotoDateView(object):
    queryset = Photo.objects.on_site().is_public()
    date_field = 'date_added'
    allow_empty = True


class PhotoDateDetailView(PhotoDateView, DateDetailView):
    pass


class PhotoArchiveIndexView(PhotoDateView, ArchiveIndexView):
    pass


class PhotoDayArchiveView(PhotoDateView, DayArchiveView):
    pass


class PhotoMonthArchiveView(PhotoDateView, MonthArchiveView):
    pass


class PhotoYearArchiveView(PhotoDateView, YearArchiveView):
    make_object_list = True


# Deprecated views.

class DeprecatedMonthMixin(object):

    """Representation of months in urls has changed from a alpha representation ('jan' for January)
    to a numeric representation ('01' for January).
    Properly deprecate the previous urls."""

    query_string = True

    month_names = {'jan': '01',
                   'feb': '02',
                   'mar': '03',
                   'apr': '04',
                   'may': '05',
                   'jun': '06',
                   'jul': '07',
                   'aug': '08',
                   'sep': '09',
                   'oct': '10',
                   'nov': '11',
                   'dec': '12', }

    def get_redirect_url(self, *args, **kwargs):
        print('a')
        warnings.warn(
            DeprecationWarning('Months are now represented in urls by numbers rather than by '
                               'their first 3 letters. The old style will be removed in Photologue 3.2.'))


class TravelogueDateDetailOldView(DeprecatedMonthMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        super(TravelogueDateDetailOldView, self).get_redirect_url(*args, **kwargs)
        return reverse('travelogue:travelogue-detail', kwargs={'year': kwargs['year'],
                                                            'month': self.month_names[kwargs['month']],
                                                            'day': kwargs['day'],
                                                            'slug': kwargs['slug']})


class TravelogueDayArchiveOldView(DeprecatedMonthMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        super(TravelogueDayArchiveOldView, self).get_redirect_url(*args, **kwargs)
        return reverse('travelogue:travelogue-archive-day', kwargs={'year': kwargs['year'],
                                                                 'month': self.month_names[kwargs['month']],
                                                                 'day': kwargs['day']})


class TravelogueMonthArchiveOldView(DeprecatedMonthMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        super(TravelogueMonthArchiveOldView, self).get_redirect_url(*args, **kwargs)
        return reverse('travelogue:travelogue-archive-month', kwargs={'year': kwargs['year'],
                                                                   'month': self.month_names[kwargs['month']]})


class PhotoDateDetailOldView(DeprecatedMonthMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        super(PhotoDateDetailOldView, self).get_redirect_url(*args, **kwargs)
        return reverse('travelogue:photo-detail', kwargs={'year': kwargs['year'],
                                                          'month': self.month_names[kwargs['month']],
                                                          'day': kwargs['day'],
                                                          'slug': kwargs['slug']})


class PhotoDayArchiveOldView(DeprecatedMonthMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        super(PhotoDayArchiveOldView, self).get_redirect_url(*args, **kwargs)
        return reverse('travelogue:photo-archive-day', kwargs={'year': kwargs['year'],
                                                               'month': self.month_names[kwargs['month']],
                                                               'day': kwargs['day']})


class PhotoMonthArchiveOldView(DeprecatedMonthMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        super(PhotoMonthArchiveOldView, self).get_redirect_url(*args, **kwargs)
        return reverse('travelogue:photo-archive-month', kwargs={'year': kwargs['year'],
                                                                 'month': self.month_names[kwargs['month']]})
