from django.contrib import admin
from .models import Post,Comment, Author, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('name',  'category')
    list_filter = ['name']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)