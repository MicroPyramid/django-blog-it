from django import forms
from .models import Post, Category, Page, Menu, ContactUsSettings, ROLE_CHOICE, Theme
from django.template.defaultfilters import slugify
# for authentication
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICE, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'is_active')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if self.instance.id:
            if User.objects.filter(email=email, username=username).exclude(id=self.instance.id).count():
                raise forms.ValidationError(u'Email addresses must be unique.')
        else:
            if User.objects.filter(email=email).exclude(username=username).count():
                raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        for field in iter(self.fields):
            if max(enumerate(iter(self.fields)))[0] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    "placeholder": "Please enter your " + field.capitalize()
                })

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Incorrect Login Details")

        return self.cleaned_data


class BlogPostForm(forms.ModelForm):
    tags = forms.CharField(label="Tags", max_length=300, required=False)

    class Meta:
        model = Post
        exclude = ('slug', 'user', 'tags')

    def __init__(self, *args, **kwargs):
        self.user_role = kwargs.pop('user_role', None)
        super(BlogPostForm, self).__init__(*args, **kwargs)

        if self.user_role == 'Author':
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
        self.fields['category'].queryset = Category.objects.filter(is_active=True)

    def clean_status(self):
        if self.user_role == "Author":
            raise forms.ValidationError("Admin and Publisher can change status only.")
        return self.cleaned_data.get("status")


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
            if max(enumerate(iter(self.fields)))[0] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', "placeholder": "Please enter your Category " + field.capitalize()
                })


class UserRoleForm(forms.Form):
    role = forms.CharField(max_length=10)


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ('slug',)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            if max(enumerate(iter(self.fields)))[0] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', "placeholder": "Please enter your Page " + field.capitalize()
                })

    def clean_title(self):
        if not self.instance.id:
            if self.Meta.model.objects.filter(slug=slugify(self.cleaned_data['title'])).exists():
                raise forms.ValidationError('Page with this title already exists.')
        else:
            if self.Meta.model.objects.filter(title__icontains=self.cleaned_data['title']).exclude(id=self.instance.id):
                raise forms.ValidationError('Page with this title already exists.')

        return self.cleaned_data['title']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('lvl',)

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            if max(enumerate(iter(self.fields)))[0] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', "placeholder": "Please enter your Menu " + field.capitalize()
                })


class ContactUsSettingsForm(forms.ModelForm):

    class Meta:
        model = ContactUsSettings
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ContactUsSettingsForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if max(enumerate(iter(self.fields)))[0] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    "placeholder": "Please enter your " + field.replace('_', ' ').capitalize()
                })


class BlogThemeForm(forms.ModelForm):

    class Meta:
        model = Theme
        exclude = ('slug',)
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BlogThemeForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                "placeholder": "Please enter your Theme " + field.capitalize()
            })


class ContactForm(forms.Form):
    contact_name = forms.CharField(max_length=128, required=True)
    contact_email = forms.EmailField(required=True)
    contact_website = forms.URLField(
        max_length=200, required=True, help_text="Enter Your Website URL here")
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        contact_website = cleaned_data.get('contact_website')

        if contact_website and not contact_website.startswith('http://'):
            contact_website = 'http://' + contact_website
            cleaned_data['contact_website'] = contact_website

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].widget.attrs['placeholder'] = "Enter Your Name (Required)"
        self.fields['contact_email'].widget.attrs['placeholder'] = "Enter Your Email (Required)"
        self.fields['contact_website'].widget.attrs['placeholder'] = "Enter Your Website (Required)"
        self.fields['content'].widget.attrs['placeholder'] = "What do you want to say?"
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!!!")
        return confirm_password


class CustomBlogSlugInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(CustomBlogSlugInlineFormSet, self).clean()
        if any(self.errors):
            return
        active_slugs = 0
        for form in self.forms:
            if form.cleaned_data.get("is_active"):
                active_slugs += 1
        if active_slugs > 1:
            raise forms.ValidationError("Only one slug can be active at a time.")
