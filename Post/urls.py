from django.contrib import admin
from django.urls import path
from Post import views

urlpatterns = [
    path('createPost/', views.CreatePostView.as_view()),
    path('updatePost/<int:pk>/', views.UpdatePostView.as_view()),
    path('updatePostStatus/<int:pk>/', views.UpdateRentStatusView.as_view()),
    path('hostPostList/', views.HostPostListView.as_view()),
    path('postDetail/<int:pk>/', views.PostDetailView.as_view()),
]
