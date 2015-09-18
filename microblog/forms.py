from django.forms import forms, ModelForm
from .models import Post, Category


class BlogPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('slug', 'tags', 'user',)


class BlogCategory(ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)