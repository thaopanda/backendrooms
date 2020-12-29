from django.contrib import admin
from django.urls import path
from Post import views

urlpatterns = [
    path('createPost/', views.CreatePostView.as_view()),
    path('updatePost/<int:pk>/', views.UpdatePostView.as_view()),
    path('updatePostStatus/<int:pk>/', views.UpdateRentStatusView.as_view()),
    path('hostPostList/', views.HostPostListView.as_view()),
    path('postDetail/<int:pk>/', views.PostDetailView.as_view()),
    path('extendExpiredDate/<int:pk>/', views.ExtendExpiredDateView.as_view()),
    path('homePage/<str:location>/<int:begin>/<int:end>/', views.HomePageView.as_view()),
    path('search/<str:searching>/<int:begin>/<int:end>/', views.Search.as_view()),
    # path('searchByCiteria/<str:address>/<str:describeAddress>/<int:price>/<str:roomType>/<int:square>/<str:kitchen>/<str:bathroom>/<str:heater>/<str:airconditioner>/<int:begin>/<int:end>/', views.SearchByCiteria.as_view()),
    path('admin/confirmpost/<int:pk>/', views.ConfirmedPost.as_view()),
    path('admin/postList/<str:confirm>/<int:begin>/<int:end>/', views.PostList.as_view()),
    path('searchByCiteria/', views.SearchByCiteria.as_view()),
    
]
