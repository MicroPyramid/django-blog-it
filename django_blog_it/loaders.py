import os
from django.conf import settings
from django.template.loaders.base import Loader as BaseLoader

from django.template import TemplateDoesNotExist
from django_blog_it.models import Theme


class Loader(BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):

        themes = Theme.objects.filter(enabled=True)
        for theme in themes:
            filepath = os.path.join(os.path.dirname(__file__), 'themes', theme.name, 'templates', template_name)
            try:
                file = open(filepath)
                try:
                    return (file.read().decode(settings.FILE_CHARSET), filepath)
                finally:
                    file.close()
            except IOError:
                pass

        raise TemplateDoesNotExist("Could not find template '%s'." % template_name)
