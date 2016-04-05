from django.contrib import admin
from .models import Post, Category, Tags


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'is_active')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'category', 'status')


class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tags, TagsAdmin)
