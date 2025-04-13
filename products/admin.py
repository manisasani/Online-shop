from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Product, Comment, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


class CommentsInline(admin.TabularInline):
    model = Comment
    fields = ['author', 'body', 'stars', 'active',]
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'active',]
    list_filter = ['category', 'active']
    search_fields = ['title', 'description']
    inlines = [CommentsInline,]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'body', 'stars', 'active',]