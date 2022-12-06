from django.db import models
from ..users.models import User


# Create your models here.
class Post(models.Model):
    titulo = models.CharField(
        verbose_name='Titulo',
        max_length=300, unique=True, blank=False, null=False
    )

    sub_titulo = models.CharField(
        verbose_name="Sub titulo",
        max_length=300, blank=False, null=False
    )

    contenido = models.TextField(
        verbose_name='Contenido',
        blank=False, null=False
    )

    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    fecha_creacion = models.DateTimeField(
        verbose_name='Fecha de Creacion',
        auto_now_add=True
    )

    image_post = models.CharField(
        verbose_name='Url imagen',
        max_length=300)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'{self.fecha_creacion} {self.titulo}'


