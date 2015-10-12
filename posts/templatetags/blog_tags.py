import datetime
from django import template
from microblog.models import Post, Tags

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_archives(context):
    archives = []
    dates = []
    for each_object in Post.objects.filter(category__is_active=True, status="Published").order_by('created_on').values('created_on'):
        for date in each_object.values():
            dates.append((date.year, date.month, 1))

    dates = list(set(dates))
    dates.sort(reverse=True)
    for each in dates:
        archives.append(datetime.datetime(each[0], each[1], each[2]))

    if len(archives) > 5:
        return archives[:5]
    return archives


@register.filter
def seperate_tags(tags):
    tags_list = tags.split(',')
    real_tags = []
    for tag in tags_list:
        real_tags.append(Tags.objects.get(name=tag))
    return real_tags
