from datetime import datetime
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django_blog_it.django_blog_it.models import Post, Category, Tags, Page
from django.db.models import Count
from django_blog_it import settings
from django.http import Http404


def categories_tags_lists():
    categories_list = Category.objects.filter(is_active=True, post__status='Published').distinct()
    tags_list = Tags.objects.annotate(
                    Num=Count('rel_posts')
                ).filter(Num__gt=0, rel_posts__status='Published', rel_posts__category__is_active=True)[:20]
    posts = Post.objects.filter(status='Published').order_by('-updated_on')[0:3]
    cat_tags = {'categories_list': categories_list, 'tags_list': tags_list, 'recent_posts': posts}
    return cat_tags


# def seperate_tags():
#     posts_tags = Post.objects.filter(category__is_active=True, status='Published')
#     for blog in posts_tags:
#         blog_tags_new = blog.tags.split(',')
#         for tag in blog_tags_new:
#             real_tags = Tags.objects.get(slug=tag)
#             return real_tags


def index(request):
    blog_posts = Post.objects.filter(status='Published', category__is_active=True).order_by('-updated_on')
    # blog_posts = [post for post in blog_posts if post.category.is_active]
    context = list({'blog_posts': blog_posts}.items()) + list(categories_tags_lists().items())
    seo = [
        ("description", settings.BLOG_DESCRIPTION),
        ("title", settings.BLOG_TITLE),
        ("keywords", settings.BLOG_KEYWORDS),
        ("author", settings.BLOG_AUTHOR),
    ]
    context += seo
    return render(request, 'posts/index.html', context)


def blog_post_view(request, blog_slug):
    blog_name = get_object_or_404(Post, slug=blog_slug)  # Post.objects.get(slug=blog_slug)
    related_posts = Post.objects.filter(
        status='Published', category=blog_name.category,
        tags__in=blog_name.tags.all()).exclude(id=blog_name.id).distinct()[:3]
    context = list({'blog_name': blog_name}.items()) + \
        list(categories_tags_lists().items()) + \
        list({'related_posts': related_posts}.items()) + \
        list({'disqus_shortname': getattr(settings, 'DISQUS_SHORTNAME')}.items())
    user = blog_name.user
    author = user.first_name if user.first_name else user.username
    seo = [
        ("description", blog_name.meta_description if blog_name.meta_description else ""),
        ("title", blog_name.title),
        ("keywords", blog_name.keywords),
        ("author", author),
    ]
    context += seo
    return render(request, 'posts/blog_view.html', context)


def selected_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    blog_posts = Post.objects.filter(category__slug=category_slug, category__is_active=True, status='Published')
    context = list({'blog_posts': blog_posts}.items()) + list(categories_tags_lists().items())
    user = category.user
    author = user.first_name if user.first_name else user.username
    seo = [
        ("description", category.description),
        ("title", category.name),
        ("keywords", category.meta_keywords),
        ("author", author),
    ]
    context += seo
    return render(request, 'posts/index.html', context + [("category", category)])


def selected_tag(request, tag_slug):
    tag = get_object_or_404(Tags, slug=tag_slug)
    blog_posts = get_list_or_404(
        Post, tags__slug=tag_slug,
        status='Published', category__is_active=True
    )
    context = list({'blog_posts': blog_posts}.items()) + list(categories_tags_lists().items()) + [("tag", tag)]
    seo = [
        ("description", tag.name),
        ("title", tag.name),
        ("keywords", tag.name),
        ("author", settings.BLOG_AUTHOR),
    ]
    context += seo
    return render(request, 'posts/index.html', context)


def archive_posts(request, year, month):
    date = datetime(int(year), int(month), 1)
    blog_posts = Post.objects.filter(
        category__is_active=True,
        status="Published",
        updated_on__year=year,
        updated_on__month=month
    ).order_by('-updated_on')
    blog_posts = [post for post in blog_posts if post.category.is_active]
    context = list({'blog_posts': blog_posts}.items()) + list(categories_tags_lists().items()) + [("date", date)]
    seo = [
        ("description", "Blog Archive - " + date.strftime("%B %Y")),
        ("title", "Blog Archive - " + date.strftime("%B %Y")),
        ("keywords", "Blog Archive - " + date.strftime("%B %Y")),
        ("author", settings.BLOG_AUTHOR),
    ]
    context += seo
    return render(request, 'posts/index.html', context)


def page_view(request, page_slug):
    pages = Page.objects.filter(slug=page_slug)
    if pages:
        context = list({'page': pages[0]}.items())
        return render(request, 'posts/page.html', context)
    raise Http404
