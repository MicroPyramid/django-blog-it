from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from microblog.models import Post, Category, Tags, Image_File, STATUS_CHOICE

import datetime
import calendar


# Create your views here.
def archives_months():
    cur_month = datetime.date.today().month
    cur_year = datetime.date.today().year

    archives_list = []
    for i in range(5):
        if cur_month == 0:
            cur_month = 12
            cur_year -= 1

        archives_list.append({'year': cur_year, 'month': cur_month})
        # archives_list.append({'year': cur_year, 'month': calendar.month_name[cur_month]})
        cur_month -= 1

    return archives_list


def categories_tags_lists():
    categories_list = Category.objects.all()
    tags_list = Tags.objects.all()
    cat_tags = {'categories_list': categories_list, 'tags_list': tags_list}
    return cat_tags


def index(request):
    blog_posts = Post.objects.all().order_by('-updated_on')
    context = {'blog_posts': blog_posts, 'archives_list': archives_months()}.items() + categories_tags_lists().items()
    return render(request, 'posts/index.html', context)


def selected_category(request, category_slug):
    blog_posts = Post.objects.filter(category__slug=category_slug)
    context = {'blog_posts': blog_posts, 'archives_list': archives_months()}.items() + categories_tags_lists().items()
    return render(request, 'posts/index.html', context)


def selected_tag(request, tag_slug):
    tag_name = Tags.objects.get(slug=tag_slug)
    blog_posts = Post.objects.filter(tags__icontains=tag_name)
    context = {'blog_posts': blog_posts, 'archives_list': archives_months()}.items() + categories_tags_lists().items()
    return render(request, 'posts/index.html', context)


def archive_posts(request, year, month):
    blog_posts = Post.objects.filter(status="Published", updated_on__year=year, updated_on__month=month).order_by('-updated_on')
    print blog_posts
    context = {'blog_posts': blog_posts, 'archives_list': archives_months()}.items() + categories_tags_lists().items()
    return render(request, 'posts/index.html', context)