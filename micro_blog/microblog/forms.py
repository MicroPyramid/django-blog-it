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

        return self.cleaned_data


class BlogPostForm(forms.ModelForm):
    tags = forms.CharField(label="Tags", max_length=300, required=False)

    class Meta:
        model = Post
        exclude = ('slug', 'user', 'tags')

    def __init__(self, *args, **kwargs):
        self.is_superuser = kwargs.pop('is_superuser', None)
        self.user_role = kwargs.pop('user_role', None)
        super(BlogPostForm, self).__init__(*args, **kwargs)
        if self.is_superuser or self.user_role != 'Author':
            pass
        else:
            del self.fields['status']
        for field in iter(self.fields):

            if field == 'tags':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control myTags', "placeholder": "Please enter your Blog " + field.capitalize()
                })

            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', "placeholder": "Please enter your Blog " + field.capitalize()
                })


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)

    def clean_name(self):
        if not self.instance.id:
            if Category.objects.filter(slug=slugify(self.cleaned_data['name'])).exists():
                raise forms.ValidationError('Category with this Name already exists.')
        else:
            if Category.objects.filter(name__icontains=self.cleaned_data['name']).exclude(id=self.instance.id):
                raise forms.ValidationError('Category with this Name already exists.')

        return self.cleaned_data['name']

    def __init__(self, *args, **kwargs):
        super(BlogCategoryForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            if max(enumerate(iter(self.fields)))[1] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', "placeholder": "Please enter your Category " + field.capitalize()
                })


class UserRoleForm(forms.Form):
    role = forms.CharField(max_length=10)
