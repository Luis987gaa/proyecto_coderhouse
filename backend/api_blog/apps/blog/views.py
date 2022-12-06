from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from .models import Post


class PostAPIView(generics.RetrieveAPIView):
    """ Obtiene todas las publicaiones en registradas en la base de datos. """
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()


class PostListAPIView(generics.ListAPIView):
    """ Obtiene todas las publicaiones en registradas en la base de datos. """
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        model = self.serializer_class().Meta.model
        return model.objects.all()


class PostUserListAPIView(generics.ListAPIView):
    """ Obtiene todas las publicaiones en registradas en la base de datos de un solo usuario. """
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        model = self.serializer_class().Meta.model
        return model.objects.filter(autor=self.kwargs['pk']).all()


class PostCreateAPIView(generics.CreateAPIView):
    """ Clase para la creacion de publicaciones solo para administradores y usuarios logeados. """
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated)

    def get_queryset(self):
        model = self.serializer_class().Meta.model
        return model.objects.all()


class PostsUpdateAPIView(generics.UpdateAPIView):
    """ Clase para la modificacion de publicaciones solo para administradores y usuarios logeados. """
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated)

    def get_queryset(self):
        model = self.get_serializer().Meta.model
        return model.objects.filter(id=self.kwargs['pk']).first()

    def put(self, request, *args, **kwargs):
        if self.get_queryset():
            serializer = self.serializer_class(instance=self.get_queryset(), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "El post no existe o se ha eliminado."
            }, status = status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        if self.get_queryset():
            serializer = self.serializer_class(instance=self.get_queryset(), data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data}, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'paso'}, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
