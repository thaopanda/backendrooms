from django.contrib import admin
from django.urls import path
from Views import views

urlpatterns = [
    path('statistic/<int:pk>/', views.ViewsOnPost.as_view()),
]
