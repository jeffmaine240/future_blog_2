from django.contrib import admin
from .models import Author, BlogPost, Tag, Comment, Profile
# from django.contrib.auth.models import User


# # Register your models here.

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created", "updated")
    list_filter = ("tag","created")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title',)
    date_hierarchy = "created"
    ordering = ('-created',)
    filter_horizontal = ('tag',)
    raw_id_fields = ('author',)

class UserAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('email', 'name')
     
admin.site.register(Profile)    
admin.site.register(Author)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
