from django.urls import path
from . import views

urlpatterns = [
    path('<int:movie_id>/', views.getMovies),
    path('genre/', views.get_genre),
    path('genreSelect/', views.genre_select),
    path('like/<int:movie_id>/', views.movie_like),
    path('review/<int:movie_id>/', views.review),
    path('weather/<int:genre_id>/', views.weather),
    path('search/', views.search),
]