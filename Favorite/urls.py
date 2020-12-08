from django.contrib import admin
from django.urls import path
from Favorite import views

urlpatterns = [
    path('add/', views.CreateFavoriteView.as_view()),
    path('delete/<int:pk>/', views.DeleteFavoriteView.as_view()),
    path('list/', views.FavoriteList.as_view()),
    path('count/<int:pk>/', views.FavoriteCountView.as_view()),
]
