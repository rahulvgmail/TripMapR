import random
from django import template

register = template.Library()

from ..models import Travelogue
from ..models import Photo


@register.inclusion_tag('travelogue/tags/next_in_travelogue.html')
def next_in_travelogue(photo, travelogue):
    return {'photo': photo.get_next_in_travelogue(travelogue)}


@register.inclusion_tag('travelogue/tags/prev_in_travelogue.html')
def previous_in_travelogue(photo, travelogue):
    return {'photo': photo.get_previous_in_travelogue(travelogue)}


@register.simple_tag
def cycle_lite_travelogue(travelogue_title, height, width):
    """Generate image tags for jquery slideshow travelogue.
    See http://malsup.com/jquery/cycle/lite/"""
    html = ""
    first = 'class="first"'
    for p in Travelogue.objects.get(title=travelogue_title).public():
        html += u'<img src="%s" alt="%s" height="%s" width="%s" %s />' % (
            p.get_display_url(), p.title, height, width, first)
        first = None
    return html


@register.tag
def get_photo(parser, token):
    """Get a single photo from the travelogue library and return the img tag to display it.

    Takes 3 args:
    - the photo to display. This can be either the slug of a photo, or a variable that holds either a photo instance or
      a integer (photo id)
    - the photosize to use.
    - a CSS class to apply to the img tag.
    """
    try:
        # Split the contents of the tag, i.e. tag name + argument.
        tag_name, photo, photosize, css_class = token.split_contents()
    except ValueError:
        msg = '%r tag requires 3 arguments' % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    return PhotoNode(photo, photosize[1:-1], css_class[1:-1])


class PhotoNode(template.Node):

    def __init__(self, photo, photosize, css_class):
        self.photo = photo
        self.photosize = photosize
        self.css_class = css_class

    def render(self, context):
        try:
            a = template.resolve_variable(self.photo, context)
        except:
            a = self.photo
        if isinstance(a, Photo):
            p = a
        else:
            try:
                p = Photo.objects.get(slug=a)
            except Photo.DoesNotExist:
                # Ooops. Fail silently
                return None
        if not p.is_public:
            return None
        func = getattr(p, 'get_%s_url' % (self.photosize), None)
        if func is None:
            return 'A "%s" photo size has not been defined.' % (self.photosize)
        else:
            return u'<img class="%s" src="%s" alt="%s" />' % (self.css_class, func(), p.title)


@register.tag
def get_rotating_photo(parser, token):
    """Pick at random a photo from a given travelogue and return the img tag to display it.

    Takes 3 args:
    - the travelogue to pick a photo from. This can be either the slug of a travelogue, or a variable that holds either a
      travelogue instance or a travelogue slug.
    - the photosize to use.
    - a CSS class to apply to the img tag.
    """
    try:
        # Split the contents of the tag, i.e. tag name + argument.
        tag_name, travelogue, photosize, css_class = token.split_contents()
    except ValueError:
        msg = '%r tag requires 3 arguments' % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    return PhotoTravelogueNode(travelogue, photosize[1:-1], css_class[1:-1])


class PhotoTravelogueNode(template.Node):

    def __init__(self, travelogue, photosize, css_class):
        self.travelogue = travelogue
        self.photosize = photosize
        self.css_class = css_class

    def render(self, context):
        try:
            a = template.resolve_variable(self.travelogue, context)
        except:
            a = self.travelogue
        if isinstance(a, Travelogue):
            g = a
        else:
            try:
                g = Travelogue.objects.get(slug=a)
            except Travelogue.DoesNotExist:
                return None
        photos = g.public()
        if len(photos) > 1:
            r = random.randint(0, len(photos) - 1)
            p = photos[r]
        elif len(photos) == 1:
            p = photos[0]
        else:
            return None
        func = getattr(p, 'get_%s_url' % (self.photosize), None)
        if func is None:
            return 'A "%s" photo size has not been defined.' % (self.photosize)
        else:
            return u'<img class="%s" src="%s" alt="%s" />' % (self.css_class, func(), p.title)
