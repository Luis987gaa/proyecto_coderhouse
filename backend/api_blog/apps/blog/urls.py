from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListAPIView.as_view(), name="publicaciones"),
    path('posts/user/<int:pk>', views.PostUserListAPIView.as_view(), name="mis-publicaciones"),
    path('post/<int:pk>', views.PostAPIView.as_view(), name="obtener-publicacion"),
    path('post/create', views.PostCreateAPIView.as_view(), name="registro-publicacion"),
    path('post/update/<int:pk>', views.PostsUpdateAPIView.as_view(), name="actualizacion-publicacion"),
    path('post/delete/<int:pk>', views.PostDeleteAPIView.as_view(), name="borrar-publicacion")
]
