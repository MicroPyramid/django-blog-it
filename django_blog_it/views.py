from django.shortcuts import render, get_object_or_404, redirect
from django_blog_it.models import (BlogUser, Category, Tag, Article)
from django_blog_it.forms import CategoryForm, ArticleForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import get_user_model


def required_roles(roles):
    def user_role(function):
        def wrap(request, *args, **kwargs):
            user = BlogUser.objects.filter(
                user=request.user, is_active=True).values_list(
                'role', flat=True)
            for role in user:
                if (role in roles) or (
                        'admin' in roles and request.user.is_superuser):
                    return function(request, *args, **kwargs)
            raise Http404
        return wrap
    return user_role


@login_required
def dashboard(request):
    return render(request, 'django_blog_it/admin/dashboard.html')


@login_required
@required_roles(["admin", 'blog_admin'])
def user_list(request):
    total_users = get_user_model().objects.all()
    page = request.GET.get('page', 1)
    if request.GET.get('name'):
        name = request.GET.get('name')
        total_users = total_users.filter(email__icontains=name)
    if request.GET.get('page_length'):
        length = request.GET.get('page_length')
    else:
        length = 15
    paginator = Paginator(total_users, length)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'django_blog_it/admin/user_list.html',
                  {'users': users, 'list_length': length})


@login_required
@required_roles(["admin", 'blog_admin'])
def user_role(request):
    if request.method == "POST":
        role = request.POST.get('role')
        user = request.POST.get('user_id')
        if role:
            if not BlogUser.objects.filter(user_id=user, role=role).exists():
                BlogUser.objects.create(user_id=user, role=role)
        return JsonResponse({"response": 'done'})
    else:
        user_id = request.GET.get('user_id')
        role = request.GET.get('role')
        blog = BlogUser.objects.filter(user_id=user_id, role=role).first()
        blog.delete()
        return JsonResponse({"response": 'done'})


@login_required
@required_roles(["admin", "blog_admin", 'blog_publisher', 'blog_author'])
def blog_list(request):
    article_data = Article.objects.order_by('id')
    if request.GET.get('name'):
        name = request.GET.get('name')
        article_data = article_data.filter(
            title__icontains=name)
    blogs_list = article_data.filter(is_page=False)
    pages_list = article_data.filter(is_page=True)
    return render(
        request, 'django_blog_it/admin/blog_list.html', {'blogs_list': blogs_list, 'pages_list': pages_list})


@login_required
@required_roles(["admin", 'blog_admin', 'blog_publisher', 'blog_author'])
def blog_new(request):
    category_list = Category.objects.filter(created_by=request.user)
    tag_ids = Article.objects.values_list("tags", flat=True)
    tags = Tag.objects.filter(id__in=tag_ids)
    if request.method == 'POST':
        form = ArticleForm(request.POST, type=request.POST.get('is_page'))
        if form.is_valid():
            blog = form.save(commit=False)
            blog.created_by = request.user
            if request.POST.get('category'):
                blog.category = Category.objects.filter(
                    id=request.POST['category']).first()
            if request.POST.get('is_page') == "Page":
                blog.is_page = True
            else:
                blog.is_page = False
            blog.save()
            if request.POST.getlist('tags'):
                splitted_tags = request.POST.getlist("tags")
                for t in splitted_tags:
                    tag = Tag.objects.filter(name=t.lower())
                    if tag:
                        tag = tag[0]
                    else:
                        tag = Tag.objects.create(name=t.lower())
                    blog.tags.add(tag)
            return redirect('django_blog_it:blog_list')
        return render(request, 'django_blog_it/admin/blog_new.html', {'category': category_list, 'form': form.errors, 'tags': tags})
    return render(request, 'django_blog_it/admin/blog_new.html', {'category': category_list, 'tags': tags})


@login_required
@required_roles(["admin", 'blog_admin', 'blog_publisher', 'blog_author'])
def blog_edit(request, pk):
    blog_content = get_object_or_404(Article, id=pk)
    category_list = Category.objects.filter(
        created_by=request.user)
    tag_ids = Article.objects.filter(
        created_by=request.user).values_list("tags", flat=True)
    tags = Tag.objects.filter(id__in=tag_ids)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=blog_content,
                           type=request.POST.get('is_page'))
        if form.is_valid():
            blog = form.save(commit=False)
            if request.POST.get("is_page") == "Page":
                blog.is_page = True
            else:
                blog.is_page = False
            blog.save()
            if request.POST.getlist('tags'):
                blog_content.tags.clear()
                tags = request.POST.getlist('tags')
                for t in tags:
                    tag = Tag.objects.filter(name=t.lower())
                    if tag:
                        tag = tag[0]
                    else:
                        tag = Tag.objects.create(name=t.lower())
                    blog.tags.add(tag)
            return redirect('django_blog_it:blog_list')
        return render(request, 'django_blog_it/admin/blog_edit.html', {'form': form.errors, 'blog': blog_content, 'category': category_list, 'tags': tags})
    return render(request, 'django_blog_it/admin/blog_edit.html', {'blog': blog_content, 'category': category_list, 'tags': tags})


@login_required
@required_roles(["admin", 'blog_admin', 'blog_publisher', 'blog_author'])
def blog_delete(request, pk):
    blog = get_object_or_404(Article, id=pk)
    blog.delete()
    return redirect('django_blog_it:blog_list')


@login_required
@required_roles(["admin", 'blog_admin', 'blog_publisher', 'blog_author'])
def blog_category_list(request):
    category_list = Category.objects.order_by('id')
    page = request.GET.get('page', 1)
    if request.GET.get('name'):
        name = request.GET.get('name')
        category_list = category_list.filter(name__icontains=name)
    if request.GET.get('page_length'):
        length = request.GET.get('page_length')
    else:
        length = 15
    paginator = Paginator(category_list, length)
    try:
        blog = paginator.page(page)
    except PageNotAnInteger:
        blog = paginator.page(1)
    except EmptyPage:
        blog = paginator.page(paginator.num_pages)
    return render(request, 'django_blog_it/admin/blog_category_list.html', {'blogdata': blog, 'list_length': length})


@login_required
@required_roles(["admin", 'blog_admin', 'blog_publisher', 'blog_author'])
def blog_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.created_by = request.user
            blog.is_active = True
            blog.save()
            return redirect('django_blog_it:blog_category_list')
        return render(request, 'django_blog_it/admin/blog_category_create.html', {'form': form.errors
                                                                                  })
    return render(request, 'django_blog_it/admin/blog_category_create.html')


@login_required
@required_roles(["admin", 'blog_admin', 'blog_publisher', 'blog_author'])
def blog_catergory_edit(request, pk):
    blog = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('django_blog_it:blog_category_list')
        return render(request, 'django_blog_it/admin/blog_category_edit.html',
                      {'form': form.errors, 'blog_data': blog})
    return render(request, 'django_blog_it/admin/blog_category_edit.html', {'blog_data': blog})


@login_required
@required_roles(["admin", 'blog_admin', 'blog_publisher', 'blog_author'])
def blog_category_delete(request, pk):
    blog = get_object_or_404(Category, id=pk)
    blog.delete()
    return redirect('django_blog_it:blog_category_list')


@login_required
@required_roles(["admin", 'blog_admin', 'blog_publisher', 'blog_author'])
def page_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.created_by = request.user
            blog.is_active = True
            blog.is_page = True
            blog.save()
            return redirect('django_blog_it:page_category_list')
        return render(request, 'django_blog_it/admin/page_category.html', {'form': form.errors
                                                                           })
    return render(request, 'django_blog_it/admin/page_category.html')


@login_required
def blog_detail(request, slug):
    blog = get_object_or_404(Article, slug=slug, is_page=False)
    return render(request, 'django_blog_it/blog/blog.html', {'data': blog})


@login_required
def blog_preview(request, pk):
    blog = get_object_or_404(Article, id=pk)
    return render(request, 'django_blog_it/admin/preview.html', {'data': blog})


@login_required
def page_detail(request, slug):
    blog = get_object_or_404(Article, slug=slug, is_page=True)
    return render(request, 'django_blog_it/page/page.html', {'data': blog})


@login_required
def blog_content_edit_with_grapejs(request, pk):
    blog = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        landinpage_url = reverse(
            "django_blog_it:get_blog_content", kwargs={"pk": pk}
        )
        return render(
            request,
            "django_blog_it/admin/grape_js.html",
            {"landinpage_url": landinpage_url},
        )
    if request.method == "POST":
        html = request.POST.get("html")
        css = request.POST.get("css")
        if html and css:
            html_css = html + "<style>" + css + "</style>"
            blog.content = html_css
            blog.save()
        url = reverse("django_blog_it:blog_edit", kwargs={"pk": pk})
        return JsonResponse({"redirect_url": url})


@login_required
def get_blog_content(request, pk):
    blog = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        html = blog.content
        return JsonResponse({"html": html})
    return render(request, 'django_blog_it/admin/preview.html', {"data": blog})


@login_required
def blog_content_edit_with_ckeditor(request, pk):
    blog = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(
            request,
            "django_blog_it/admin/ckeditor.html", {"blog": blog}
        )
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            blog.content = content
            blog.save()
        url = reverse("django_blog_it:blog_edit", kwargs={"pk": pk})
        return JsonResponse({"redirect_url": url})
