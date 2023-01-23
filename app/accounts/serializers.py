from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from datetime import date

from .models import Author, User


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(max_length=20, write_only=True)
    password_2 = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Author
        exclude = ['user']

    def validate(self, data):
        if data['password'] != data['password_2']:
            raise serializers.ValidationError("Пароли должны совпадать")
        return data

    def create(self, validated_data):
        try:
            user = User(username=validated_data['username'])
            user.set_password(validated_data['password'])
            user.save()
        except Exception as e:
            raise serializers.ValidationError(f'Не удалось создать user {e}')
        else:
            author = Author.objects.create(
                user=user,
                telegram_chat_id=validated_data['telegram_chat_id'],
                email=validated_data['email'],
            )
            return author