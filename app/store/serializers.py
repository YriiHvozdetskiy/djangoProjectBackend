from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


class BookReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BookSerializer(ModelSerializer):
    annotation_likes = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(source='owner.username',
                                       read_only=True,
                                       default='')
    readers = BookReaderSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id',
                  'name',
                  'price',
                  'author_name',
                  'annotation_likes',
                  'owner_name',
                  'readers')


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        # нема поля user тому що це api для user
        fields = ('book', 'like', 'in_bookmarks', 'rate')
