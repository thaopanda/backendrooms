from django.contrib import admin
from django.urls import path
from Review import views

urlpatterns = [
    path('createReview/<int:pk>/', views.CreateReviewView.as_view()),
    path('delete/<int:pk>/', views.DeleteReviewView.as_view()),
    path('listReviewOfPost/<int:pk>/<int:begin>/<int:end>/', views.ListReviewOfPost.as_view()),
    path('listReviewOfRenter/', views.ListReviewOfRenter.as_view()),
    path('listReview/', views.ListReview.as_view()),
    path('confirmReview/<int:pk>/', views.ConfirmReview.as_view()),
]
