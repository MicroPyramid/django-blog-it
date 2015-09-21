from django.forms import forms, ModelForm
from .models import Post, Category
from django.template.defaultfilters import slugify


class BlogPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('slug', 'tags', 'user',)


class BlogCategory(ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)

    def clean_name(self):
        clean_data = self.cleaned_data

        if Category.objects.filter(slug=slugify(clean_data['name'])).exists():
            raise forms.ValidationError('Slug already created with this name')
        return clean_data['name']

