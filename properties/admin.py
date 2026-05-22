from django.contrib import admin
from .models import Property, PropertyImage, Favorite, UserProfile


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'listing_type', 'property_type', 'city', 'price', 'is_active', 'is_featured']
    list_filter = ['listing_type', 'property_type', 'is_active', 'is_featured']
    search_fields = ['title', 'city', 'address']
    inlines = [PropertyImageInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'property']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
