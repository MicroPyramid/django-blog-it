from django.forms import forms, ModelForm
from .models import Post, Category
from django.template.defaultfilters import slugify


class BlogPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('slug', 'tags', 'user',)


class BlogCategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)

    # def clean_name(self):
    #     clean_data = self.cleaned_data
    #     if Category.objects.filter(name__icontains=clean_data['name']).exists():
    #         raise forms.ValidationError('Name already exists')
    #     return clean_data['name']

    # def __init__(self, *args, **kwargs):
    #     super(BlogCategoryForm, self).__init__(*args, **kwargs)
    #
    # def save(self):
    #     instance = super(BlogCategoryForm, self).save(commit=False)
    #     form_data = self.cleaned_data
    #     instance.slug= slugify(form_data['name'])
    #     instance.save()
    #     return instance

