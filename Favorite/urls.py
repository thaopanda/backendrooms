from django.contrib import admin
from django.urls import path
from Favorite import views

urlpatterns = [
    path('createAndDelete/<int:pk>/', views.CreateAndDeleteFavoriteView.as_view()),
    path('list/<int:begin>/<int:end>/', views.FavoriteList.as_view()),
    path('count/<int:pk>/', views.FavoriteCountView.as_view()),
]
