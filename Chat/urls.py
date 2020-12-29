from django.contrib import admin
from django.urls import path, include
from Chat import views

urlpatterns = [
    path('thread/', views.GetThread.as_view()),
    path('chat/<int:pk>/<int:begin>/<int:end>/', views.GetChat.as_view()),
    path('threadAdmin/<str:username>/', views.GetThreadAdmin.as_view()),

]
 