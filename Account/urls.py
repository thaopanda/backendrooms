from django.contrib import admin
from django.urls import path
from Account import views

urlpatterns = [
    path('renterregister/', views.RenterRegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('hostregister/', views.HostRegistrationView.as_view()),
    path('renterProfile/', views.RenterProfileView.as_view()),
    path('hostProfile/', views.HostProfileView.as_view()),
    path('renterUpdateProfile/', views.RenterUpdateProfileView.as_view()),
    path('hostUpdateProfile/', views.HostUpdateProfileView.as_view()),
    path('changePassword/', views.ChangePasswordView.as_view()),
    path('allUser/', views.AllUser.as_view()),
    path('admin/confirmedhostlist/<int:begin>/<int:end>/', views.GetListHost.as_view()),
    path('admin/unconfirmedhostlist/<int:begin>/<int:end>/', views.GetUnconfirmedHost.as_view()),
    path('admin/confirmhost/<int:pk>/', views.ConfirmedHostAccount.as_view()),
    path('admin/allowupdate/<int:pk>/', views.AllowUpdatePermission.as_view()),

]
