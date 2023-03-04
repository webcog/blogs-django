from django.contrib import admin
from .models import Category, Post, Profile
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description','profile_image']
admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'updated_at', 'created_by', 'category', 'slug', 'post_image',]
    prepopulated_fields = {"slug": ("title","category", "created_by")}
admin.site.register(Post, PostAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'bio', 'location', 'birth_date', 'website']
admin.site.register(Profile, ProfileAdmin)


