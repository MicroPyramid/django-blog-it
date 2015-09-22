from django import forms
from .models import Post, Category
from django.template.defaultfilters import slugify
# for authentication
from django.contrib.auth import authenticate


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Incorrect login details")
            if not user.is_staff:
                raise forms.ValidationError('You are not allowed to this page')

        return self.cleaned_data


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('slug', 'tags', 'user',)


class BlogCategoryForm(forms.ModelForm):
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
