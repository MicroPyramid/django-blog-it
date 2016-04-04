import json
from PIL import Image
import os
import requests

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

from .models import Post, PostHistory, Category, Tags, Image_File, STATUS_CHOICE, ROLE_CHOICE, UserRole
from .forms import BlogCategoryForm, BlogPostForm, AdminLoginForm, UserRoleForm
from django_blog_it import settings
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

admin_required = user_passes_test(lambda user: user.is_active, login_url='/dashboard')


def active_admin_required(view_func):
    decorated_view_func = login_required(admin_required(view_func), login_url='/dashboard')
    return decorated_view_func


def admin_login(request):
    if request.user.is_active:
        return HttpResponseRedirect('/dashboard/blog')
    if request.method == 'POST':
        login_form = AdminLoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user.is_active:
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
    if request.method == "POST":
        if request.POST.get('select_status', ''):
            blog_list = blog_list.filter(status=request.POST.get('select_status'))
        if request.POST.get('search_text'):
            blog_list = blog_list.filter(
                title__icontains=request.POST.get('search_text')
            ) | blog_list.filter(
                tags__name__icontains=request.POST.get('search_text')
            )

    context = {'blog_list': blog_list.distinct(), 'blog_choices': STATUS_CHOICE}
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
        request.POST = request.POST.copy()
        if request.POST.get('title') == '':
            request.POST['title'] = 'Untitled document ' + str(Post.objects.all().count())
        form = BlogPostForm(
                request.POST,
                is_superuser=request.user.is_superuser,
                user_role=get_user_role(request.user)
            )
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            # for autosave
            if request.user.is_superuser:
                blog_post.status = request.POST.get('status')
            blog_post.save()

            if request.POST.get('tags', ''):
                tags = request.POST.get('tags')
                splitted = tags.split(',')
                for s in splitted:
                    blog_tags = Tags.objects.filter(name__iexact=s.strip())
                    if blog_tags:
                        blog_tag = blog_tags.first()
                    else:
                        blog_tag = Tags.objects.create(name=s.strip())
                    blog_post.tags.add(blog_tag)

            blog_post.create_activity(user=request.user, content="added")
            messages.success(request, 'Successfully posted your blog')
            data = {'error': False, 'response': 'Successfully posted your blog', 'title': request.POST['title']}
        else:
            data = {'error': True, 'response': form.errors, 'title': request.POST['title']}
        return HttpResponse(json.dumps(data))
    context = {'form': form, 'status_choices': STATUS_CHOICE, 'categories_list': categories_list,
               'tags_list': tags_list, 'add_blog': True}
    return render(request, 'dashboard/blog/blog_add.html', context)


@active_admin_required
def edit_blog(request, blog_slug):
    blog_name = Post.objects.get(slug=blog_slug)
    if blog_name.user == request.user or request.user.is_superuser is True or get_user_role(request.user) != 'Author':
        form = BlogPostForm(
                instance=blog_name,
                is_superuser=request.user.is_superuser, user_role=get_user_role(request.user),
                initial={'tags': ','.join([tag.name for tag in blog_name.tags.all()])}
            )

        categories_list = Category.objects.filter(is_active=True)
        if request.method == "POST":
            previous_status = blog_name.status
            form = BlogPostForm(
                    request.POST,
                    instance=blog_name,
                    is_superuser=request.user.is_superuser,
                    user_role=get_user_role(request.user)
                )
            if form.is_valid():
                blog_post = form.save(commit=False)
                blog_post.user = request.user
                if request.user.is_superuser or get_user_role(request.user) != 'Author':
                    blog_post.status = request.POST.get('status')
                else:
                    blog_post.status = previous_status
                blog_post.save()
                blog_post.tags.clear()
                if request.POST.get('tags', ''):
                    tags = request.POST.get('tags')
                    splitted = tags.split(',')
                    for s in splitted:
                        blog_tags = Tags.objects.filter(name__iexact=s.strip())
                        if blog_tags:
                            blog_tag = blog_tags.first()
                        else:
                            blog_tag = Tags.objects.create(name=s.strip())
                        blog_post.tags.add(blog_tag)

                if blog_post.status == previous_status:
                    blog_post.create_activity(user=request.user, content="updated")
                else:
                    blog_post.create_activity(
                        user=request.user,
                        content="changed status from " +
                        str(previous_status) + " to " + str(blog_post.status)
                    )
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
    if request.method == "POST" and request.POST.get("action"):
        blog_post = get_object_or_404(Post, slug=blog_slug)
        if blog_post.is_deletable_by(request.user) or request.user.is_superuser is True or get_user_role(request.user) != 'Author':
            previous_status = blog_post.status
            if request.POST.get("action") == "trash":
                blog_post.status = "Trashed"
                blog_post.save()
                blog_post.create_activity(
                    user=request.user,
                    content="moved to trash from " + str(previous_status)
                )
                messages.success(
                    request,
                    'Blog "' + str(blog_post.title) + '" has been moved to trash.'
                )
            elif request.POST.get("action") == "restore":
                blog_post.status = "Drafted"
                blog_post.save()
                blog_post.create_activity(
                    user=request.user,
                    content="restored from trash to " + str(blog_post.status)
                )
                messages.success(
                    request,
                    'Blog "' + str(blog_post.title) + '" has been restored from trash.'
                )
            elif request.POST.get("action") == "delete":
                blog_post.remove_activity()
                blog_post.delete()
                messages.success(request, 'Blog successfully deleted')
            else:
                raise Http404
        else:
            raise Http404
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
    if category_name.user == request.user or request.user.is_superuser is True:
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
    if category.user == request.user or request.user.is_superuser is True:
        category.delete()
        return HttpResponseRedirect('/dashboard/category/')


@active_admin_required
def bulk_actions_blog(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            if 'blog_ids[]' in request.GET:
                blog_posts = Post.objects.filter(id__in=request.GET.getlist('blog_ids[]'))
                if request.GET.get('action') in [status[0] for status in STATUS_CHOICE]:
                    history_list = []
                    for blog in blog_posts:
                        history_list.append(
                            blog.create_activity_instance(
                                user=request.user,
                                content="changed status from " + str(blog.status) +
                                " to " + str(request.GET.get('action'))
                            )
                        )
                    blog_posts.update(status=request.GET.get('action'))
                    PostHistory.objects.bulk_create(history_list)
                    messages.success(
                        request, 'Selected blog posts' +
                        ' successfully updated as ' + str(request.GET.get('action'))
                    )

                elif request.GET.get('action') == 'Delete':
                    PostHistory.objects.filter(post__in=blog_posts).delete()
                    blog_posts.delete()

                return HttpResponse(json.dumps({'response': True}))
            else:
                messages.warning(request, 'Please select at-least one record to perform this action')
                return HttpResponse(json.dumps({'response': False}))


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


@csrf_exempt
def upload_photos(request):
    '''
    takes all the images coming from the redactor editor and
    stores it in the database and returns all the files
    '''
    upurl = ''
    if request.FILES.get("upload"):
        f = request.FILES.get("upload")
        obj = Image_File.objects.create(upload=f, is_image=True)
        obj.save()
        thumbnail_name = 'thumb' + f.name
        if getattr(settings, 'AWS_ENABLED', 'False'):
            image_file = requests.get(obj.upload.url, stream=True)
            with open(thumbnail_name, 'wb') as destination:
                for chunk in image_file.iter_content():
                    destination.write(chunk)
        else:
            image_file = f
            with open(thumbnail_name, 'wb') as destination:
                for chunk in image_file.chunks():
                    destination.write(chunk)
        im = Image.open(destination.name)
        size = (128, 128)
        im.thumbnail(size)
        im.save(thumbnail_name)
        imdata = open(thumbnail_name)
        obj.thumbnail.save(thumbnail_name, File(imdata))
        obj.save()
        os.remove(os.path.join(settings.BASE_DIR, thumbnail_name))
        upurl = obj.upload.url
    return HttpResponse(
            """<script type='text/javascript'>
            window.parent.CKEDITOR.tools.callFunction({0}, '{1}');
            </script>""".format(request.GET['CKEditorFuncNum'], upurl)
        )


def get_user_role(user):
    user_role = UserRole.objects.filter(user=user)
    if user_role:
        return user_role[0].role
    return 'No User Role'


@csrf_exempt
def recent_photos(request):
    ''' returns all the images from the data base '''

    imgs = []
    for obj in Image_File.objects.filter(is_image=True).order_by("-date_created"):
        upurl = obj.upload.url
        thumburl = obj.thumbnail.url
        imgs.append({'src': upurl, 'thumb': thumburl, 'is_image': True})
    return render_to_response('dashboard/browse.html', {'files': imgs})


@active_admin_required
def users(request):
    users_list = User.objects.all()
    if request.method == 'POST':
        if 'select_role' in request.POST.keys() and request.POST.get('select_role'):
            users_list = []
            user_roles = UserRole.objects.filter(role=request.POST.get('select_role'))
            for role in user_roles:
                users_list.append(role.user)
    context = {'users_list': users_list, 'roles': ROLE_CHOICE}
    return render(request, 'dashboard/user/list.html', context)


def delete_user(request, pk):
    users = User.objects.filter(pk=pk)
    if users:
        user = users[0]
        user.delete()
    else:
        raise Http404
    return HttpResponseRedirect(reverse('users'))


def edit_user_role(request, pk):
    user_role = UserRole.objects.filter(user_id=pk)
    if request.method == 'GET':
        context = {'user_role': user_role, 'roles': ROLE_CHOICE}
        return render(request, 'dashboard/user/user_role.html', context)
    validate_user_role = UserRoleForm(request.POST)
    if validate_user_role.is_valid():
        if user_role:
            user_role = user_role[0]
            user_role.role = request.POST.get('role')
            user_role.save()
        else:
            user = User.objects.get(pk=pk)
            UserRole.objects.create(user=user, role=request.POST.get('role'))
        messages.success(request, 'Successfully Updated User Role')
        data = {'error': False, 'response': 'Successfully Updated User Role'}
    else:
        data = {'error': True, 'response': validate_user_role.errors}
    return HttpResponse(json.dumps(data))
