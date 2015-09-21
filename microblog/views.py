import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Category, Tags, Image_File, STATUS_CHOICE
from .forms import BlogCategoryForm, BlogPostForm
from django.template.defaultfilters import slugify


# Create your views here.


def blog(request):
    blog_list = Post.objects.all()
    context = {'blog_list': blog_list}
    return render(request, 'blog_list.html', context)


def view_blog(request, blog_id):
    blog_name = Post.objects.get(id=blog_id)
    context = {'blog_name': blog_name}
    return render(request, 'blog_view.html', context)


def blog_add(request):
    categories_list = Category.objects.all()
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            blog_post.status = 'D'
            if request.POST.get('status') == 'P':
                blog_post.status = 'P'
            elif request.POST.get('status') == 'T':
                blog_post.status = 'T'
            blog_post.save()

            data = {'error': False, 'response': 'Successfully posted your blog'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'status_choices': STATUS_CHOICE, 'categories_list': categories_list}
    return render(request, 'blog_add.html', context)


def edit_blog(request, blog_id):
    blog_name = Post.objects.get(id=blog_id)
    categories_list = Category.objects.all()
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=blog_name)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            blog_post.status = 'D'
            if request.POST.get('status') == 'P':
                blog_post.status = 'P'
            elif request.POST.get('status') == 'T':
                blog_post.status = 'T'
            blog_post.save()

            data = {'errors': False, 'response': 'Successfully updated your blog post'}
        else:
            data = {'errors': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'blog_name': blog_name, 'status_choices': STATUS_CHOICE, 'categories_list': categories_list}
    return render(request, 'blog_add.html', context)


def delete_blog(request, blog_id):
    blog_name = Post.objects.get(id=blog_id)
    blog_name.delete()
    return HttpResponseRedirect('/blog/')


def categories(request):
    categories_list = Category.objects.all()
    context = {'categories_list': categories_list}
    return render(request, 'categories_list.html', context)


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


def edit_category(request, category_id):
    category_name = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category_data = request.POST
        form = BlogCategoryForm(category_data, instance=category_name)
        if form.is_valid():
            form.save()
            data = {'error': False, 'response': 'Successfully updated your category'}
        else:
            data = {'error': True, 'response': form.errors}
        return HttpResponse(json.dumps(data))
    context = {'category_name': category_name}
    return render(request, 'category_add.html', context)


def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return HttpResponseRedirect('/blog/category/')
