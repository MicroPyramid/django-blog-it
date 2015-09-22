import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Category, Tags, Image_File, STATUS_CHOICE
from .forms import BlogCategoryForm, BlogPostForm, AdminLoginForm
from django.template.defaultfilters import slugify

# for admin-login and logout
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required

admin_required = user_passes_test(lambda user: user.is_staff, login_url='/')


def active_admin_required(view_func):
    decorated_view_func = login_required(admin_required(view_func), login_url='/')
    return decorated_view_func


def admin_login(request):
    if request.user.is_staff:
        return HttpResponseRedirect('/blog')
    if request.method == 'POST':
        login_form = AdminLoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user.is_staff:
                login(request, user)
                response_data = {'error': False, 'response': 'Successfully logged in'}
            else:
                response_data = {'error': True, 'response': 'You are not allowed to this page'}
            return HttpResponse(json.dumps(response_data))
        else:
            response_data = {'error': True, 'response': login_form.errors}

        return HttpResponse(json.dumps(response_data))

    return render(request, 'admin-login.html')


@active_admin_required
def admin_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@active_admin_required
def blog(request):
    blog_list = Post.objects.all()
    context = {'blog_list': blog_list}
    return render(request, 'blog_list.html', context)


@active_admin_required
def view_blog(request, blog_id):
    blog_name = Post.objects.get(id=blog_id)
    context = {'blog_name': blog_name}
    return render(request, 'blog_view.html', context)


@active_admin_required
def blog_add(request):
    categories_list = Category.objects.all()
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            blog_post.status = 'Drafted'
            if request.POST.get('status') == 'Published':
                blog_post.status = 'Published'
            elif request.POST.get('status') == 'Rejected':
                blog_post.status = 'Rejected'
            blog_post.save()

            data = {'error': False, 'response': 'Successfully posted your blog'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'status_choices': STATUS_CHOICE, 'categories_list': categories_list}
    return render(request, 'blog_add.html', context)


@active_admin_required
def edit_blog(request, blog_id):
    blog_name = Post.objects.get(id=blog_id)
    categories_list = Category.objects.all()
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=blog_name)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            blog_post.status = 'Drafted'
            if request.POST.get('status') == 'Published':
                blog_post.status = 'Published'
            elif request.POST.get('status') == 'Rejected':
                blog_post.status = 'Rejected'
            blog_post.save()

            data = {'errors': False, 'response': 'Successfully updated your blog post'}
        else:
            data = {'errors': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'blog_name': blog_name, 'status_choices': STATUS_CHOICE, 'categories_list': categories_list}
    return render(request, 'blog_add.html', context)


@active_admin_required
def delete_blog(request, blog_id):
    blog_name = Post.objects.get(id=blog_id)
    blog_name.delete()
    return HttpResponseRedirect('/blog/')


@active_admin_required
def categories(request):
    categories_list = Category.objects.all()
    context = {'categories_list': categories_list}
    return render(request, 'categories_list.html', context)


@active_admin_required
def add_category(request):
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST)
        if form.is_valid():
            form.save()

            data = {'error': False, 'response': 'Successfully added your category'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    return render(request, 'category_add.html')


@active_admin_required
def edit_category(request, category_slug):
    category_name = Category.objects.get(slug=category_slug)
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST, instance=category_name)
        if form.is_valid():
            form.save()

            data = {'error': False, 'response': 'Successfully updated your category'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'category_name': category_name}
    return render(request, 'category_add.html', context)


@active_admin_required
def delete_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    category.delete()
    return HttpResponseRedirect('/blog/category/')


@active_admin_required
def bulk_actions_blog(request):
    if request.method == 'GET':
        if 'blog_ids[]' in request.GET:

            if request.GET.get('action') == 'Published' or request.GET.get('action') == 'Drafted' or request.GET.get(
                    'action') == 'Rejected':
                Post.objects.filter(id__in=request.GET.getlist('blog_ids[]')).update(
                    status=request.GET.get('action'))

            if request.GET.get('action') == 'Delete':
                Post.objects.filter(id__in=request.GET.getlist('blog_ids[]')).delete()

            return HttpResponse(json.dumps({'response': 'success'}))
        else:
            return HttpResponse(json.dumps({'response': 'fail'}))

    return render(request, '/blog/')


@active_admin_required
def bulk_actions_category(request):
    if request.method == 'GET':
        if 'blog_ids[]' in request.GET:
            if request.GET.get('action') == 'True':
                Category.objects.filter(id__in=request.GET.getlist('blog_ids[]')).update(
                    is_active=True)
            if request.GET.get('action') == 'False':
                Category.objects.filter(id__in=request.GET.getlist('blog_ids[]')).update(
                    is_active=False)

            if request.GET.get('action') == 'Delete':
                Category.objects.filter(id__in=request.GET.getlist('blog_ids[]')).delete()

            return HttpResponse(json.dumps({'response': 'success'}))
        else:
            return HttpResponse(json.dumps({'response': 'fail'}))

    return render(request, '/blog/category/')
