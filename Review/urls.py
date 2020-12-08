from django.contrib import admin
from django.urls import path
from Review import views

urlpatterns = [
    path('createReview/', views.CreateReviewView.as_view()),
    path('delete/<int:pk>/', views.DeleteReviewView.as_view()),
    path('listReviewOfPost/<int:pk>/', views.ListReviewOfPost.as_view()),
    path('listReviewOfRenter/', views.ListReviewOfRenter.as_view()),
]
