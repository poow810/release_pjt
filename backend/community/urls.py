from django.urls import path
from . import views

urlpatterns = [
    path('', views.post),
    path('create/', views.post),
    path('detail/<int:post_id>/', views.detail),
    path('detail/like/<int:post_id>/', views.detail_like),
    path('edit/<int:post_id>/', views.editPost),
    path('comments/<int:post_id>/', views.comment),
    path('comments/<int:post_id>/<int:comment_id>/', views.commentUpdate),
    path('comments/delete/<int:comment_id>/', views.commentDelete),
]
