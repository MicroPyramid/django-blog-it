import json
from PIL import Image
import os
import requests
from django.db.models.aggregates import Max
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

from .models import Menu, Post, PostHistory, Category, Tags, Image_File, \
    STATUS_CHOICE, ROLE_CHOICE, UserRole, Page, Theme
from .forms import *
from django_blog_it import settings
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView,\
    UpdateView, View
from .mixins import AdminMixin, PostAccessRequiredMixin
from django.http import JsonResponse

admin_required = user_passes_test(lambda user: user.is_active, login_url='/')


def active_admin_required(view_func):
    decorated_view_func = login_required(admin_required(view_func), login_url='/')
    return decorated_view_func


def admin_login(request):
    if request.user.is_active:
        return HttpResponseRedirect(reverse('blog'))
    if request.method == 'POST':
        login_form = AdminLoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            if user.is_active:
                login(request, user)
                messages.success(request, 'You are successfully logged in')
                response_data = {'error': False,
                                 'response': 'Successfully logged in'}
            else:
                response_data = {'error': True,
                                 'response': 'You are not allowed to this page'}
            return HttpResponse(json.dumps(response_data))
        else:
            response_data = {'error': True, 'response': login_form.errors}

        return HttpResponse(json.dumps(response_data))

    return render(request, 'dashboard/new_admin-login.html')


@active_admin_required
def admin_logout(request):
    logout(request)
    messages.success(request, 'You are successfully logged out!')
    return HttpResponseRedirect(reverse('admin_login'))


class PostList(AdminMixin, ListView):
    model = Post
    template_name = 'dashboard/blog/new_blog_list.html'
    context_object_name = 'blog_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['blog_choices'] = STATUS_CHOICE
        context['object_list'] = self.model.objects.all()
        context['published_blogs'] = self.model.objects.filter(
            status='Published')
        return context

    def post(self, request, *args, **kwargs):
        blog_list = self.model.objects.all()

        if request.POST.get('select_status', ''):
            blog_list = blog_list.filter(
                status=request.POST.get('select_status')
            )
        if request.POST.get('search_text', ''):
            blog_list = blog_list.filter(
                title__icontains=request.POST.get('search_text')
            ) | blog_list.filter(
                tags__name__icontains=request.POST.get('search_text')
            )
        return render(request, self.template_name,
                      {'blog_list': blog_list, 'blog_choices': STATUS_CHOICE})


class PostDetailView(DetailView):
    model = Post
    template_name = 'dashboard/blog/new_blog_view.html'
    slug_field = "slug"
    context_object_name = 'blog_post'

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['blog_slug'])


class PostCreateView(AdminMixin, CreateView):
    model = Post
    form_class = BlogPostForm
    template_name = "dashboard/blog/new_blog_add.html"
    success_url = '/dashboard/blog/'

    def form_valid(self, form):
        self.blog_post = form.save(commit=False)
        self.blog_post.user = self.request.user

        if self.request.user.is_superuser:
            self.blog_post.status = self.request.POST.get('status')
        self.blog_post.save()

        if self.request.POST.get('tags', ''):
            splitted = self.request.POST.get('tags').split(',')
            for s in splitted:
                blog_tags = Tags.objects.filter(name__iexact=s.strip())
                if blog_tags:
                    blog_tag = blog_tags.first()
                else:
                    blog_tag = Tags.objects.create(name=s.strip())
                self.blog_post.tags.add(blog_tag)

        self.blog_post.create_activity(user=self.request.user, content="added")
        messages.success(self.request, 'Successfully posted your blog')
        data = {'error': False, 'response': 'Successfully posted your blog',
                'title': self.request.POST['title']}
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse({'error': True, 'response': form.errors})

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        form = BlogPostForm(self.request.GET,
                            is_superuser=self.request.user.is_superuser)
        tags_list = Tags.objects.all()
        categories_list = Category.objects.filter(is_active=True)

        context['form'] = form
        context['status_choices'] = STATUS_CHOICE

        context['categories_list'] = categories_list
        context['tags_list'] = tags_list
        context['add_blog'] = True
        return context


class PostEditView(UpdateView):
    model = Post
    success_url = '/dashboard/blog/'
    slug_field = 'slug'
    template_name = "dashboard/blog/new_blog_add.html"
    form_class = BlogPostForm

    def dispatch(self, request, *args, **kwargs):
        if request.POST:
            instance = self.get_object()
            if request.POST.get("history_id"):
                history_post = instance.history.filter(id=request.POST.get("history_id")).last()
                if history_post:
                    return JsonResponse({"content": history_post.content})
        return super(PostEditView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['blog_slug'])

    def form_invalid(self, form):
        return JsonResponse({'error': True, 'response': form.errors})

    def form_valid(self, form):
        previous_status = self.get_object().status
        previous_content = self.get_object().content
        self.blog_post = form.save(commit=False)
        self.blog_post.user = self.request.user
        if self.request.user.is_superuser or get_user_role(self.request.user) != 'Author':
            self.blog_post.status = self.request.POST.get('status')
        else:
            self.blog_post.status = previous_status
        self.blog_post.save()
        self.blog_post.tags.clear()
        if self.request.POST.get('tags', ''):
            splitted = self.request.POST.get('tags').split(',')
            for s in splitted:
                blog_tags = Tags.objects.filter(name__iexact=s.strip())
                if blog_tags:
                    blog_tag = blog_tags.first()
                else:
                    blog_tag = Tags.objects.create(name=s.strip())
                self.blog_post.tags.add(blog_tag)
        if previous_content != self.blog_post.content:
            self.blog_post.create_activity(
                user=self.request.user, content=previous_content)
        # if self.blog_post.status == previous_status:
        #     self.blog_post.create_activity(
        #         user=self.request.user, content="updated")
        # else:
        #     self.blog_post.create_activity(
        #         user=self.request.user,
        #         content="changed status from " +
        #         str(previous_status) + " to " + str(blog_post.status)
        #     )

        messages.success(self.request, 'Successfully updated your blog post')
        data = {'error': False,
                'response': 'Successfully updated your blog post'}
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super(PostEditView, self).get_context_data(**kwargs)
        form = BlogPostForm(instance=self.get_object(),
                            is_superuser=self.request.user.is_superuser,
                            user_role=get_user_role(self.request.user),
                            initial={'tags': ','.join([tag.name for tag in self.get_object().tags.all()])}
                            )
        categories_list = Category.objects.filter(is_active=True)

        context['form'] = form
        context['blog_name'] = self.get_object()
        context['status_choices'] = STATUS_CHOICE,
        context['categories_list'] = categories_list
        context['history_list'] = self.get_object().history.all()
        return context


class PostDeleteView(PostAccessRequiredMixin, DeleteView):
    model = Post
    success_url = '/dashboard/blog/'
    slug_field = 'slug'
    template_name = "dashboard/blog/new_blog_list.html"

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs['blog_slug'])

    def post(self, request, *args, **kwargs):
        blog_post = self.get_object()
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
            return HttpResponseRedirect(self.success_url)
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
            return HttpResponseRedirect(self.success_url)
        elif request.POST.get("action") == "delete":
            blog_post.remove_activity()
            blog_post.delete()
            messages.success(request, 'Blog successfully deleted')
            return HttpResponseRedirect(self.success_url)
        else:
            raise Http404


@active_admin_required
def categories(request):
    categories_list = Category.objects.all()
    category_choices = categories_list
    context = {'categories_list': categories_list,
               'category_choices': category_choices}

    if request.method == "POST":
        requested_categories = request.POST.getlist('category')

        if request.POST.get('select_status', ''):
            if request.POST.get('select_status') == "True":
                categories_list = categories_list.filter(is_active=True)
            else:
                categories_list = categories_list.filter(is_active=False)

        if request.POST.get('search_text'):
            categories_list = categories_list.filter(
                name__icontains=request.POST.get('search_text')
            )

        context = {'categories_list': categories_list,
                   'requested_categories': requested_categories,
                   'category_choices': category_choices}
    return render(request,
                  'dashboard/category/new_categories_list.html',
                  context)


@active_admin_required
def add_category(request):
    form = BlogCategoryForm()
    if request.method == 'POST':
        form = BlogCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added your category')
            data = {'error': False,
                    'response': 'Successfully added your category'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'form': form, 'add_category': True}
    return render(request, 'dashboard/category/new_category_add.html', context)


@active_admin_required
def edit_category(request, category_slug):
    category_name = get_object_or_404(Category, slug=category_slug) # Category.objects.get(slug=category_slug)
    if category_name.user == request.user or request.user.is_superuser is True:
        form = BlogCategoryForm(instance=category_name)

        if request.method == 'POST':
            form = BlogCategoryForm(request.POST, instance=category_name)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully updated your category')
                data = {'error': False,
                        'response': 'Successfully updated your category'}
            else:
                data = {'error': True, 'response': form.errors}
            return HttpResponse(json.dumps(data))
        context = {'form': form, 'category_name': category_name}
        return render(request,
                      'dashboard/category/new_category_add.html', context)


@active_admin_required
def delete_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug) # Category.objects.get(slug=category_slug)
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
                messages.warning(
                    request,
                    'Please select at-least one record to perform this action')
                return HttpResponse(json.dumps({'response': False}))


@active_admin_required
def bulk_actions_category(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            if 'blog_ids[]' in request.GET:
                if request.GET.get('action') == 'True':
                    Category.objects.filter(
                        id__in=request.GET.getlist('blog_ids[]')).update(
                        is_active=True)
                    messages.success(
                        request,
                        'Selected Categories successfully updated as Active')
                elif request.GET.get('action') == 'False':
                    Category.objects.filter(
                        id__in=request.GET.getlist('blog_ids[]')).update(
                        is_active=False)
                    messages.success(
                        request,
                        'Selected Categories successfully updated as Inactive')

                elif request.GET.get('action') == 'Delete':
                    Category.objects.filter(
                        id__in=request.GET.getlist('blog_ids[]')).delete()
                    messages.success(
                        request,
                        'Selected Categories successfully deleted!')

                return HttpResponse(json.dumps({'response': True}))
            else:
                messages.warning(
                    request,
                    'Please select at-least one record to perform this action')
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
            user_roles = UserRole.objects.filter(
                role=request.POST.get('select_role')
            )
            for role in user_roles:
                users_list.append(role.user)
        if request.POST.get('search_text'):
            users = User.objects.all()
            users_list = users.filter(
                username__icontains=request.POST.get('search_text')
            ) | users.filter(
                email__icontains=request.POST.get('search_text')
            ) | users.filter(
                first_name__icontains=request.POST.get('search_text')
            ) | users.filter(
                last_name__icontains=request.POST.get('search_text')
            )
    context = {'users_list': users_list, 'roles': ROLE_CHOICE}
    return render(request, 'dashboard/user/new_list.html', context)


@active_admin_required
def add_user(request):
    form = UserForm()
    form_errors = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        validate_user_role = UserRoleForm(request.POST)
        if form.is_valid() and validate_user_role.is_valid():
            user = form.save()
            UserRole.objects.create(user=user, role=request.POST.get('role'))
            messages.success(request, 'Successfully added your User')
            data = {'error': False, 'response': 'Successfully added your User'}
        else:
            form_errors['user_form'] = form.errors
            form_errors['user_role_form'] = validate_user_role.errors
            data = {'error': True, 'response': form_errors}
        return HttpResponse(json.dumps(data))
    context = {'form': form, 'roles': ROLE_CHOICE, 'add_user': True}
    return render(request, 'dashboard/user/new_add_user.html', context)


@active_admin_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_role = UserRole.objects.filter(user_id=pk)
    form = UserForm(instance=user)
    form_errors = {}
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        validate_user_role = UserRoleForm(request.POST)
        if form.is_valid() and validate_user_role.is_valid():
            user = form.save()
            if user_role:
                user_role = user_role[0]
                user_role.role = request.POST.get('role')
                user_role.save()
            else:
                user = User.objects.get(pk=pk)
                UserRole.objects.create(user=user,
                                        role=request.POST.get('role'))
            messages.success(request, 'Successfully Updated User "' + str(user) + '"')
            data = {'error': False, 'response': 'Successfully Updated User "' + str(user) + '"'}
        else:
            form_errors['user_form'] = form.errors
            form_errors['user_role_form'] = validate_user_role.errors
            data = {'error': True, 'response': form_errors}
        return HttpResponse(json.dumps(data))
    context = {'user': user, 'user_role': user_role,
               'form': form, 'roles': ROLE_CHOICE, 'add_user': True}
    return render(request, 'dashboard/user/new_add_user.html', context)


def delete_user(request, pk):
    users = User.objects.filter(pk=pk)
    if users:
        user = users[0]
        user.delete()
    else:
        raise Http404
    return HttpResponseRedirect(reverse('users'))


@active_admin_required
def bulk_actions_users(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            if 'user_ids[]' in request.GET:
                if request.GET.get('action') == 'True':
                    User.objects.filter(
                        id__in=request.GET.getlist('user_ids[]')).update(
                        is_active=True)
                    messages.success(request, 'Selected Users successfully updated as Active')
                elif request.GET.get('action') == 'False':
                    User.objects.filter(
                        id__in=request.GET.getlist('user_ids[]')).update(
                        is_active=False)
                    messages.success(request, 'Selected Users successfully updated as Inactive')

                elif request.GET.get('action') == 'Delete':
                    User.objects.filter(
                        id__in=request.GET.getlist('user_ids[]')).delete()
                    messages.success(request, 'Selected Users successfully deleted!')

                return HttpResponse(json.dumps({'response': True}))
            else:
                messages.warning(request, 'Please select at-least one record to perform this action')
                return HttpResponse(json.dumps({'response': False}))


def edit_user_role(request, pk):
    user_role = UserRole.objects.filter(user_id=pk)
    if request.method == 'GET':
        context = {'user_role': user_role, 'roles': ROLE_CHOICE}
        return render(request, 'dashboard/user/new_user_role.html', context)
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


@active_admin_required
def pages(request):
    pages_list = Page.objects.all()
    context = {'pages_list': pages_list}

    if request.method == "POST":

        if request.POST.get('select_status', ''):
            if request.POST.get('select_status') == "True":
                pages_list = pages_list.filter(is_active=True)
            else:
                pages_list = pages_list.filter(is_active=False)
        if request.POST.get('search_text'):
            pages_list = pages_list.filter(
                title__icontains=request.POST.get('search_text')
            )

        context = {'pages_list': pages_list}
    return render(request, 'dashboard/pages/new_list.html', context)


@active_admin_required
def add_page(request):
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added your page')
            data = {'error': False, 'response': 'Successfully added your page'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'form': form}
    return render(request, 'dashboard/pages/new_add_page.html', context)


@active_admin_required
def edit_page(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug) # Page.objects.get(slug=page_slug)

    if request.user.is_superuser is True:
        form = PageForm(instance=page)

        if request.method == 'POST':
            form = PageForm(request.POST, instance=page)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully updated your page')
                data = {'error': False, 'response': 'Successfully updated your page'}
            else:
                data = {'error': True, 'response': form.errors}
            return HttpResponse(json.dumps(data))
        context = {'form': form, 'page': page}
        return render(request, 'dashboard/pages/new_add_page.html', context)


@active_admin_required
def delete_page(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)  # Page.objects.get(slug=page_slug)
    if request.user.is_superuser is True:
        page.delete()
        messages.success(request, 'Page successfully deleted!')
        return HttpResponseRedirect(reverse('pages'))
    else:
        raise Http404


@active_admin_required
def bulk_actions_pages(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            if 'page_ids[]' in request.GET:
                if request.GET.get('action') == 'True':
                    Page.objects.filter(
                        id__in=request.GET.getlist('page_ids[]')).update(
                        is_active=True)
                    messages.success(request, 'Selected Pages successfully updated as Active')
                elif request.GET.get('action') == 'False':
                    Page.objects.filter(
                        id__in=request.GET.getlist('page_ids[]')).update(
                        is_active=False)
                    messages.success(request, 'Selected Pages successfully updated as Inactive')

                elif request.GET.get('action') == 'Delete':
                    Page.objects.filter(
                        id__in=request.GET.getlist('page_ids[]')).delete()
                    messages.success(request, 'Selected Pages successfully deleted!')

                return HttpResponse(json.dumps({'response': True}))
            else:
                messages.warning(request, 'Please select at-least one record to perform this action')
                return HttpResponse(json.dumps({'response': False}))


@active_admin_required
def menus(request):
    menu_list = Menu.objects.filter(parent=None)
    context = {'menu_list': menu_list}

    if request.method == "POST":

        if request.POST.get('select_status', ''):
            if request.POST.get('select_status') == "True":
                menu_list = menu_list.filter(status=True)
            else:
                menu_list = menu_list.filter(status=False)
        if request.POST.get('search_text'):
            menu_list = menu_list.filter(
                title__icontains=request.POST.get('search_text')
            )

        context = {'menu_list': menu_list}
    return render(request, 'dashboard/menu/new_list.html', context)


@active_admin_required
def add_menu(request):
    form = MenuForm()
    if request.method == 'POST':
        form = MenuForm(request.POST)

        if form.is_valid():
            menu_obj = form.save(commit=False)
            menu_count = Menu.objects.filter(parent=menu_obj.parent).count()
            menu_obj.lvl = menu_count + 1
            if menu_obj.url[-1] != '/':
                menu_obj.url = menu_obj.url + '/'
            menu_obj.save()
            messages.success(request, 'Successfully added menu.')
            data = {'error': False, 'response': 'Successfully added menu.'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'form': form, 'add_menu': True}
    return render(request, 'dashboard/menu/new_manage.html', context)


@active_admin_required
def edit_menu(request, pk):
    menu_obj = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu_obj)
    current_parent = menu_obj.parent
    current_lvl = menu_obj.lvl

    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu_obj)
        if form.is_valid():
            updated_menu_obj = form.save(commit=False)
            if updated_menu_obj.parent != current_parent:
                if updated_menu_obj.parent.id == updated_menu_obj.id:
                    data = {'error': True, 'message': 'you can not choose the same as parent'}
                    return HttpResponse(json.dumps(data))

                menu_count = Menu.objects.filter(
                    parent=updated_menu_obj.parent).count()
                updated_menu_obj.lvl = menu_count + 1
                menu_max_lvl = Menu.objects.filter(
                    parent=current_parent).aggregate(Max('lvl'))['lvl__max']
                if menu_max_lvl != 1:
                    for i in Menu.objects.filter(parent=current_parent, lvl__gt=current_lvl, lvl__lte=menu_max_lvl):
                        i.lvl = i.lvl - 1
                        i.save()
            if updated_menu_obj.url[-1] != '/':
                updated_menu_obj.url = updated_menu_obj.url + '/'
            updated_menu_obj.save()

            messages.success(request, 'Successfully updated menu')
            data = {'error': False, 'response': 'Successfully updated menu'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'form': form, 'menu_obj': menu_obj}
    return render(request, 'dashboard/menu/new_manage.html', context)


@active_admin_required
def bulk_actions_menu(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            if 'menu_ids[]' in request.GET:
                if request.GET.get('action') == 'True':
                    Menu.objects.filter(
                        id__in=request.GET.getlist('menu_ids[]')).update(
                        status=True)
                    messages.success(request, "Selected Menu's successfully updated as Active")
                elif request.GET.get('action') == 'False':
                    Menu.objects.filter(
                        id__in=request.GET.getlist('menu_ids[]')).update(
                        status=False)
                    messages.success(request, "Selected Menu's successfully updated as Inactive")

                elif request.GET.get('action') == 'Delete':
                    Menu.objects.filter(
                        id__in=request.GET.getlist('menu_ids[]')).delete()
                    messages.success(request, "Selected Menu's successfully deleted!")

                return HttpResponse(json.dumps({'response': True}))
            else:
                messages.warning(request, 'Please select at-least one record to perform this action')
                return HttpResponse(json.dumps({'response': False}))


@active_admin_required
def configure_contact_us(request):
    contact_us_settings = ContactUsSettings.objects.all().last()
    if request.method == 'POST':
        if contact_us_settings:
            form = ContactUsSettingsForm(instance=contact_us_settings,
                                         data=request.POST
                                         )
        else:
            form = ContactUsSettingsForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully saved your contact us details.')
            data = {'error': False, 'response': 'Successfully saved your contact us details.'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    else:
        if contact_us_settings:
            form = ContactUsSettingsForm(instance=contact_us_settings)
        else:
            form = ContactUsSettingsForm()
    context = {'form': form}
    return render(request, 'dashboard/contact_us_settings.html', context)


class ThemesList(AdminMixin, ListView):
    model = Theme
    template_name = 'dashboard/themes/themes_list.html'
    context_object_name = 'themes_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ThemesList, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all()
        context['enabled_themes'] = self.model.objects.filter(
            enabled=True)
        return context

    def post(self, request, *args, **kwargs):
        themes_list = self.model.objects.all()

        if request.POST.get('select_status', ''):
            if request.POST.get('select_status') == 'True':
                themes_list = themes_list.filter(
                    enabled=True
                )
            else:
                themes_list = themes_list.filter(
                    enabled=False
                )
        if request.POST.get('search_text', ''):
            themes_list = themes_list.filter(
                name__icontains=request.POST.get('search_text')
            )
        return render(request, self.template_name,
                      {'themes_list': themes_list})


class ThemeDetailView(AdminMixin, DetailView):
    model = Theme
    template_name = 'dashboard/themes/theme_view.html'
    slug_field = "theme_slug"
    context_object_name = 'theme'

    def get_object(self):
        return get_object_or_404(Theme, slug=self.kwargs['theme_slug'])


class ThemeCreateView(AdminMixin, CreateView):
    model = Theme
    form_class = BlogThemeForm
    template_name = "dashboard/themes/theme_add.html"
    success_url = reverse_lazy('themes')

    def form_valid(self, form):
        self.blog_theme = form.save(commit=False)
        if self.request.user.is_superuser:
            self.blog_theme.enabled = self.request.POST.get('enabled')
        self.blog_theme.save()
        messages.success(self.request, 'Successfully Created your Theme')
        data = {'error': False, 'response': 'Successfully Created your Theme',
                'title': self.request.POST['name']}
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse({'error': True, 'response': form.errors})

    def get_context_data(self, **kwargs):
        context = super(ThemeCreateView, self).get_context_data(**kwargs)
        form = BlogThemeForm(self.request.GET)
        context['form'] = form
        context['add_theme'] = True
        return context


@active_admin_required
def add_theme(request):
    form = BlogThemeForm()
    if request.method == 'POST':
        form = BlogThemeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added your Theme')
            data = {'error': False,
                    'response': 'Successfully added your Theme'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'form': form, 'add_theme': True}
    return render(request, 'dashboard/themes/theme_add.html', context)


class ThemeUpdateView(AdminMixin, UpdateView):
    pk = 'pk'
    model = Theme
    form_class = BlogThemeForm
    template_name = "dashboard/themes/theme_add.html"
    success_url = reverse_lazy('themes')

    def form_valid(self, form):
        blog_theme = form.save(commit=False)
        if self.request.user.is_superuser:
            blog_theme.enabled = self.request.POST.get('enabled')
        blog_theme.save()
        messages.success(self.request, 'Successfully Updated your Theme')
        data = {'error': False, 'response': 'Successfully Updated your Theme',
                'title': self.request.POST['name']}
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse({'error': True, 'response': form.errors})


@active_admin_required
def edit_theme(request, theme_slug):
    theme = get_object_or_404(Theme, slug=theme_slug) #  Theme.objects.get(slug=theme_slug)
    if request.user.is_superuser is True:
        form = BlogThemeForm(instance=theme)

        if request.method == 'POST':
            form = BlogThemeForm(request.POST, instance=theme)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully updated your Theme')
                data = {'error': False,
                        'response': 'Successfully updated your Theme'}
            else:
                data = {'error': True, 'response': form.errors}
            return HttpResponse(json.dumps(data))
        context = {'form': form, 'theme': theme}
        return render(request,
                      'dashboard/themes/theme_add.html', context)


@active_admin_required
def delete_theme(request, theme_slug):
    theme = get_object_or_404(Theme, slug=theme_slug) #  Theme.objects.get(slug=theme_slug)
    if request.user.is_superuser is True:
        theme.delete()
        messages.success(request, 'Successfully Deleted Theme')
        return HttpResponseRedirect(reverse_lazy('themes'))


class DeleteThemeView(AdminMixin, View):

    def get(self, request, *args, **kwargs):
        theme = get_object_or_404(Theme, id=kwargs.get('pk'))
        if request.user.is_superuser is True:
            if theme:
                theme.delete()
                return HttpResponseRedirect(reverse_lazy('themes'))


@active_admin_required
def bulk_actions_themes(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            if 'theme_ids[]' in request.GET:
                if request.GET.get('action') == 'True':
                    Theme.objects.filter(
                        id__in=request.GET.getlist('theme_ids[]')).update(
                        enabled=True)
                    messages.success(request, "Selected Theme's successfully updated as Enabled")
                elif request.GET.get('action') == 'False':
                    Theme.objects.filter(
                        id__in=request.GET.getlist('theme_ids[]')).update(
                        enabled=False)
                    messages.success(request, "Selected Theme's successfully updated as Disabled")

                elif request.GET.get('action') == 'Delete':
                    Theme.objects.filter(
                        id__in=request.GET.getlist('theme_ids[]')).delete()
                    messages.success(request, "Selected Theme's successfully deleted!")

                return HttpResponse(json.dumps({'response': True}))
            else:
                messages.warning(request, 'Please select at-least one record to perform this action')
                return HttpResponse(json.dumps({'response': False}))
