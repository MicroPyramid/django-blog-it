import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required

from .models import Post, Category, Tags, Image_File, STATUS_CHOICE
from .forms import BlogCategoryForm, BlogPostForm, AdminLoginForm

admin_required = user_passes_test(lambda user: user.is_staff, login_url='/dashboard')


def active_admin_required(view_func):
    decorated_view_func = login_required(admin_required(view_func), login_url='/dashboard')
    return decorated_view_func


def admin_login(request):
    if request.user.is_staff:
        return HttpResponseRedirect('/dashboard/blog')
    if request.method == 'POST':
        login_form = AdminLoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user.is_staff:
                login(request, user)
                messages.success(request, 'You are successfully logged in')
                response_data = {'error': False, 'response': 'Successfully logged in'}
            else:
                response_data = {'error': True, 'response': 'You are not allowed to this page'}
            return HttpResponse(json.dumps(response_data))
        else:
            response_data = {'error': True, 'response': login_form.errors}

        return HttpResponse(json.dumps(response_data))

    return render(request, 'dashboard/admin-login.html')


@active_admin_required
def admin_logout(request):
    logout(request)
    messages.success(request, 'You are successfully logged out!')
    return HttpResponseRedirect('/dashboard/')


@active_admin_required
def blog(request):
    blog_list = Post.objects.all()
    blogs = blog_list
    context = {'blog_list': blog_list, 'blogs': blogs, 'blog_choices': STATUS_CHOICE}

    if request.method == "POST":
        requested_blogs = request.POST.getlist('blog')
        if request.POST.get('select_status', ''):
            blog_list = blog_list.filter(status=request.POST.get('select_status'))

        elif request.POST.getlist('blog', []):
            blog_list = blog_list.filter(id__in=request.POST.getlist('blog'))
        context = {'blog_list': blog_list, 'blogs': blogs, 'blog_choices': STATUS_CHOICE,
                   'requested_blogs': requested_blogs}
    return render(request, 'dashboard/blog/blog_list.html', context)


@active_admin_required
def view_blog(request, blog_slug):
    blog_name = Post.objects.get(slug=blog_slug)
    context = {'blog_name': blog_name}
    return render(request, 'dashboard/blog/blog_view.html', context)


@active_admin_required
def blog_add(request):
    form = BlogPostForm(request.GET, is_superuser=request.user.is_superuser)
    tags_list = Tags.objects.all()
    categories_list = Category.objects.filter(is_active=True)
    if request.method == "POST":
        form = BlogPostForm(request.POST, is_superuser=request.user.is_superuser)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            #blog_post.status = 'Drafted'
            if request.user.is_superuser:
                blog_post.status = request.POST.get('status')
            blog_post.save()

            if request.POST.get('tags', ''):
                tags = request.POST.get('tags')

                splitted = tags.split(',')
                for s in splitted:
                    final = s.strip()
                    if not Tags.objects.filter(name=final).exists():
                        Tags.objects.create(name=final)

            messages.success(request, 'Successfully posted your blog')
            data = {'error': False, 'response': 'Successfully posted your blog'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'form': form, 'status_choices': STATUS_CHOICE, 'categories_list': categories_list,
               'tags_list': tags_list, 'add_blog': True}
    return render(request, 'dashboard/blog/blog_add.html', context)


@active_admin_required
def edit_blog(request, blog_slug):
    blog_name = Post.objects.get(slug=blog_slug)
    if blog_name.user == request.user or request.user.is_superuser == True:
        form = BlogPostForm(instance=blog_name)

        categories_list = Category.objects.filter(is_active=True)
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

                if request.POST.get('tags', ''):
                    tags = request.POST.get('tags')

                    splitted = tags.split(',')
                    for s in splitted:
                        final = s.strip()
                        if not Tags.objects.filter(name=final).exists():
                            Tags.objects.create(name=final)

                messages.success(request, 'Successfully updated your blog post')
                data = {'error': False, 'response': 'Successfully updated your blog post'}
            else:
                data = {'error': True, 'response': form.errors}
            return HttpResponse(json.dumps(data))
        context = {'form': form, 'blog_name': blog_name, 'status_choices': STATUS_CHOICE,
                   'categories_list': categories_list}
        return render(request, 'dashboard/blog/blog_add.html', context)


@active_admin_required
def delete_blog(request, blog_slug):
    blog_name = Post.objects.get(slug=blog_slug)
    if blog_name.user == request.user or request.user.is_superuser == True:
        blog_name.delete()
        messages.success(request, 'Blog successfully deleted')
        return HttpResponseRedirect('/dashboard/blog/')


@active_admin_required
def categories(request):
    categories_list = Category.objects.all()
    category_choices = categories_list
    context = {'categories_list': categories_list, 'category_choices': category_choices}

    if request.method == "POST":
        requested_categories = request.POST.getlist('category')

        if request.POST.get('select_status', ''):
            if request.POST.get('select_status') == "True":
                categories_list = categories_list.filter(is_active=True)
            else:
                categories_list = categories_list.filter(is_active=False)

        elif request.POST.getlist('category', []):
            categories_list = categories_list.filter(id__in=request.POST.getlist('category'))

        context = {'categories_list': categories_list, 'requested_categories': requested_categories,
                   'category_choices': category_choices}
    return render(request, 'dashboard/category/categories_list.html', context)


@active_admin_required
def add_category(request):
    form = BlogCategoryForm()
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added your category')
            data = {'error': False, 'response': 'Successfully added your category'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'form': form, 'add_category': True}
    return render(request, 'dashboard/category/category_add.html', context)


@active_admin_required
def edit_category(request, category_slug):
    category_name = Category.objects.get(slug=category_slug)
    if category_name.user == request.user or request.user.is_superuser == True:
        form = BlogCategoryForm(instance=category_name)

        if request.method == 'POST':
            form = BlogCategoryForm(request.POST, instance=category_name)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully updated your category')
                data = {'error': False, 'response': 'Successfully updated your category'}
            else:
                data = {'error': True, 'response': form.errors}
            return HttpResponse(json.dumps(data))
        context = {'form': form, 'category_name': category_name}
        return render(request, 'dashboard/category/category_add.html', context)


@active_admin_required
def delete_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    if category.user == request.user or request.user.is_superuser == True:
        category.delete()
        return HttpResponseRedirect('/dashboard/category/')


@active_admin_required
def bulk_actions_blog(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            if 'blog_ids[]' in request.GET:

                if request.GET.get('action') == 'Published' or request.GET.get('action') == 'Drafted' or request.GET.get(
                        'action') == 'Rejected':
                    Post.objects.filter(id__in=request.GET.getlist('blog_ids[]')).update(
                        status=request.GET.get('action'))
                    messages.success(request,
                                     'Selected blog posts successfully updated as ' + str(request.GET.get('action')))

                elif request.GET.get('action') == 'Delete':
                    Post.objects.filter(id__in=request.GET.getlist('blog_ids[]')).delete()

                return HttpResponse(json.dumps({'response': True}))
            else:
                messages.warning(request, 'Please select at-least one record to perform this action')
                return HttpResponse(json.dumps({'response': False}))

        return render(request, '/dashboard/blog/')


@active_admin_required
def bulk_actions_category(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            if 'blog_ids[]' in request.GET:
                if request.GET.get('action') == 'True':
                    Category.objects.filter(id__in=request.GET.getlist('blog_ids[]')).update(
                        is_active=True)
                    messages.success(request, 'Selected Categories successfully updated as Active')
                elif request.GET.get('action') == 'False':
                    Category.objects.filter(id__in=request.GET.getlist('blog_ids[]')).update(
                        is_active=False)
                    messages.success(request, 'Selected Categories successfully updated as Inactive')

                elif request.GET.get('action') == 'Delete':
                    Category.objects.filter(id__in=request.GET.getlist('blog_ids[]')).delete()
                    messages.success(request, 'Selected Categories successfully deleted!')

                return HttpResponse(json.dumps({'response': True}))
            else:
                messages.warning(request, 'Please select at-least one record to perform this action')
                return HttpResponse(json.dumps({'response': False}))

        return render(request, '/dashboard/category/')
