from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('', views.index_page, name='index-page'),

    path('home/', views.home, name='home'),
    path('buscar/', views.search, name='buscar'),

    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),
    path('favourites/comment/', views.editComment, name='editar-comentario'),
    path('favourites/comment/delete/', views.deleteComment, name='borrar-comentario'),

    path('exit/', views.exit, name='exit'),
]
