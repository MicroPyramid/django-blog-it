from django.contrib.auth import get_user_model
from django_blog_it.models import BlogUser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create Blog User'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str, help='User ID')

    def handle(self, *args, **kwargs):
        username = kwargs["username"][0]
        if username:
            user = get_user_model().objects.filter(username=kwargs["username"][0]).first()
            if user:
                if not BlogUser.objects.filter(user_id=user, role="blog_admin").exists():
                    BlogUser.objects.create(user=user, role="blog_admin")
                print("BlogUser Created Successfully")
