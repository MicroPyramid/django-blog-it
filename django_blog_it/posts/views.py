from django.shortcuts import render, get_list_or_404
from django_blog_it.django_blog_it.models import Post, Category, Tags
from django.db.models import Count
from django.conf import settings

# Create your views here.


def categories_tags_lists():
    categories_list = Category.objects.filter(is_active=True, post__status='Published').distinct()
    tags_list = Tags.objects.annotate(
                    Num=Count('rel_posts')
                ).filter(Num__gt=0, rel_posts__status='Published')[:20]
    cat_tags = {'categories_list': categories_list, 'tags_list': tags_list}
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
    return render(request, 'posts/index.html', context)


def blog_post_view(request, blog_slug):
    blog_name = Post.objects.get(slug=blog_slug)
    context = list({'blog_name': blog_name}.items()) + \
        list(categories_tags_lists().items()) + \
        list({'disqus_shortname': settings.DISQUS_SHORTNAME}.items())
    return render(request, 'posts/blog_view.html', context)


def selected_category(request, category_slug):
    blog_posts = Post.objects.filter(category__slug=category_slug, category__is_active=True, status='Published')
    context = list({'blog_posts': blog_posts}.items()) + list(categories_tags_lists().items())
    return render(request, 'posts/index.html', context)


def selected_tag(request, tag_slug):
    blog_posts = get_list_or_404(
        Post, tags__slug=tag_slug,
        status='Published', category__is_active=True
    )
    context = list({'blog_posts': blog_posts}.items()) + list(categories_tags_lists().items())
    return render(request, 'posts/index.html', context)


def archive_posts(request, year, month):
    blog_posts = Post.objects.filter(
            category__is_active=True,
            status="Published",
            updated_on__year=year,
            updated_on__month=month
        ).order_by('-updated_on')
    blog_posts = [post for post in blog_posts if post.category.is_active]
    context = list({'blog_posts': blog_posts}.items()) + list(categories_tags_lists().items())
    return render(request, 'posts/index.html', context)
