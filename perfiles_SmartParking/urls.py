from django.urls import path

from . import views
# https://docs.djangoproject.com/en/2.2/topics/http/urls/
urlpatterns = [
    path('smartparking/<int:id>/', views.get_profile_by_id),
    path('smartparking/', views.post_profile_add),
    # path('articles/<name>/', views.get_profile_by_name),
]