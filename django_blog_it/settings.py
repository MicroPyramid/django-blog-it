from django.conf import settings

AWS_ENABLED = getattr(settings, 'AWS_ENABLED', False) 
BASE_DIR = getattr(settings, 'BASE_DIR')
MEDIA_URL = settings.MEDIA_URL
MEDIA_ROOT = settings.MEDIA_ROOT

DISQUS_SHORTNAME = getattr(settings, 'DISQUS_SHORTNAME', '') 
