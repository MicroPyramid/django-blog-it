from django import forms
from .models import Category, Article, Tag
from django.template.defaultfilters import slugify


class ArticleForm(forms.ModelForm):
    tags = forms.CharField(label="Tags", max_length=300, required=False)

    class Meta:
        model = Article
        exclude = ('created_by', 'tags', 'created_on', 'updated_on')

    def __init__(self, *args, **kwargs):
        self.user_role = kwargs.pop('user_role', None)
        self.type = kwargs.pop('type', None)
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = False

    def clean_status(self):
        if self.user_role == "Author":
            raise forms.ValidationError(
                "Admin and Publisher can change status only.")
        return self.cleaned_data.get("status")


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('slug', 'created_by')

    def clean_name(self):
        if not self.instance.id:
            if Category.objects.filter(
                    slug=slugify(self.cleaned_data['name'])).exists():
                raise forms.ValidationError(
                    'Category with this Name already exists.')
        else:
            if Category.objects.filter(
                    name__icontains=self.cleaned_data['name']).exclude(
                    id=self.instance.id):
                raise forms.ValidationError(
                    'Category with this Name already exists.')

        return self.cleaned_data['name']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CategoryForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            if max(enumerate(iter(self.fields)))[0] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    "placeholder": "Please enter your Category " + field.capitalize()
                })
