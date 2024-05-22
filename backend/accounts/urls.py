from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.profile),
    path('<int:user_id>/posts/', views.posts),
    path('<int:user_id>/movies/', views.movies),
    path('<int:user_id>/comments/', views.comments),
    path('follow/<int:user_pk>/', views.follow),
    path('change/<int:user_id>/', views.changeNickname),
]