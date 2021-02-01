from django import template
from django_blog_it.models import BlogUser

register = template.Library()


@register.simple_tag
def rolelength(user):
    role_length = BlogUser.objects.filter(
        user=user).values_list('role', flat=True).count()
    if role_length != 0:
        return True
    else:
        return False


@register.simple_tag
def adminuser(user):
    role = BlogUser.objects.filter(
        user=user, role='blog_admin').exists()
    return role


@register.filter
def get_list(dictionary, key):
    return dictionary.getlist(key)


@register.filter
def get_role_list(obj):
    return obj.values_list('role', flat=True)


@register.filter
def to_str(value):
    """converts int to string"""
    return str(value)
