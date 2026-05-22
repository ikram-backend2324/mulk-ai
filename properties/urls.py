from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('properties/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('properties/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('ai/', views.ai_assistant, name='ai_assistant'),
    path('ai/chat/', views.ai_chat, name='ai_chat'),
]
