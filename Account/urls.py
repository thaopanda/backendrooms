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
    path('allUser/<int:begin>/<int:end>/', views.AllUser.as_view()),

]
