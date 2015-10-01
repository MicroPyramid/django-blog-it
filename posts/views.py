from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from microblog.models import Post, Category, Tags, Image_File, STATUS_CHOICE

import datetime
import calendar


# Create your views here.


def categories_tags_lists():
    categories_list = Category.objects.all()
    tags_list = Tags.objects.all()
    cat_tags = {'categories_list': categories_list, 'tags_list': tags_list}
    return cat_tags


def seperate_tags():
    posts_tags = Post.objects.all()
    for blog in posts_tags:
        blog_tags_new = blog.tags.split(',')
        for tag in blog_tags_new:
            real_tags = Tags.objects.get(slug=tag)
            return real_tags


def index(request):
    blog_posts = Post.objects.all().order_by('-updated_on')
    context = {'blog_posts': blog_posts}.items() + categories_tags_lists().items()
    return render(request, 'posts/index.html', context)


def blog_post_view(request, blog_slug):
    blog_name = Post.objects.get(slug=blog_slug)
    context = {'blog_name': blog_name}.items() + categories_tags_lists().items()
    return render(request, 'posts/blog_view.html', context)


def selected_category(request, category_slug):
    blog_posts = Post.objects.filter(category__slug=category_slug)
    context = {'blog_posts': blog_posts}.items() + categories_tags_lists().items()
    return render(request, 'posts/index.html', context)


def selected_tag(request, tag_slug):
    tag_name = Tags.objects.get(slug=tag_slug)
    blog_posts = Post.objects.filter(tags__icontains=tag_name)
    context = {'blog_posts': blog_posts}.items() + categories_tags_lists().items()
    return render(request, 'posts/index.html', context)


def archive_posts(request, year, month):
    blog_posts = Post.objects.filter(status="Published", updated_on__year=year, updated_on__month=month).order_by(
        '-updated_on')
    print blog_posts
    context = {'blog_posts': blog_posts}.items() + categories_tags_lists().items()
    return render(request, 'posts/index.html', context)
