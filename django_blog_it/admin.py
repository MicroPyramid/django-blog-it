from django.contrib import admin
from .models import Article, Category, Tag, BlogUser


# class BlogAdmin(admin.ModelAdmin):
# 	list_display = ['title','category','tags','content']
# 	list_filter=('status','updated_on')
# 	ordering=['publish']

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'description', 'is_active')

# class TagsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')

admin.site.register(BlogUser)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
