from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=16)
    password2 = serializers.CharField(max_length=16)

    class Meta:
        model = User
        fields = (
            'username',
            'name',
            'last_name',
            'email',
            'password',
            'password2',
        )

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Las contraseñas no coinciden.'
            })
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)

    class Meta:
        model = User
        fields = ()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
