from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth import login
from .models import User
from .serializers import UserRegisterSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserLoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(UserLoginView, self).post(request, format=None)

    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()

        data = {
            'user_id': request.user.id,
            'msg': 'se registro el inicio de sesion correctamente.',
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data
