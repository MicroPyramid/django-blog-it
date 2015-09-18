import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Category, Tags, Image_File, STATUS_CHOICE
from .forms import BlogCategory, BlogPostForm


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
    form = BlogPostForm()
    categories_list = Category.objects.all()
    if request.method == "POST":
        blog_data = request.POST
        form = BlogPostForm(blog_data)

        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            blog_post.save()

            return HttpResponse(json.dumps({'error': False, 'response': 'Successfully posted your blog'}))
        else:
            return HttpResponse(json.dumps({'error': True, 'response': form.errors}))
    context = {'form': form, 'status_choices': STATUS_CHOICE, 'categories_list': categories_list}
    return render(request, 'blog_add.html', context)


def edit_blog(request, blog_id):
    blog_name = Post.objects.get(id=blog_id)
    categories_list = Category.objects.all()
    form = BlogPostForm()
    if request.method == "POST":
        blog_data = request.POST
        form = BlogPostForm(blog_data, instance=blog_name)

        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            blog_post.save()

            return HttpResponse(json.dumps({'errors': False, 'response': 'Successfully updated your blog post'}))
        else:
            return HttpResponse(json.dumps({'errors': True, 'response': form.errors}))
    context = {'form': form, 'blog_name': blog_name, 'status_choices': STATUS_CHOICE,
               'categories_list': categories_list}
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
    form = BlogCategory()
    if request.method == 'POST':
        category_data = request.POST
        form = BlogCategory(category_data)
        if form.is_valid():
            form.save()

            return HttpResponse(json.dumps({'error': False, 'response': 'Successfully added your category'}))
        else:
            return HttpResponse(json.dumps({'error': True, 'response': form.errors}))
    context = {'form': form}
    return render(request, 'category_add.html', context)


def edit_category(request, category_id):
    category_name = Category.objects.get(id=category_id)
    form = BlogCategory()
    if request.method == 'POST':
        category_data = request.POST
        form = BlogCategory(category_data, instance=category_name)
        if form.is_valid():
            form.save()
            return HttpResponse({'error': False, 'response': 'Successfully updated your category'})
        else:
            return HttpResponse({'error': True, 'response': form.errors})
    context = {'form': form, 'category_name':category_name}
    return render(request, 'category_add.html', context)


def delete_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category.delete()
    return HttpResponseRedirect('/blog/category/')