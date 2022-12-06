from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'titulo': instance.titulo,
            'sub_titulo': instance.sub_titulo,
            'contenido': instance.contenido,
            'autor': instance.autor.name,
            'autor_id': instance.autor.id,
            'fecha_creacion': instance.fecha_creacion,
            'image_post': instance.image_post
        }