from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('user/register/', views.UserRegisterView.as_view()),
    path('user/auth/login/', views.UserLoginView.as_view()),
    path('user/auth/logout/', knox_views.LogoutView.as_view()),
    path('user/auth/logoutall/', knox_views.LogoutView.as_view())
]
