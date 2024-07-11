from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from store.models import Book
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # IsAuthenticatedOrReadOnly - змінювати можуть тільки для аутентифікованні користувачі
    # permission_classes = [IsAuthenticatedOrReadOnly]

    # IsOwnerOrStaffOrReadOnly - персонал/адміністратор сайту може редагувати тільки свої книги
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_fields = ['price', 'author_name']

    # присвоюємо юзера до створеної книги (який створив книгу)
    def perform_create(self, serializer):
        # request.user - в запиті буде user, бо зміни може робити тільки авторизований користувач(не потрібен if)
        serializer.save(owner=self.request.user)


def auth(request):
    return render(request, 'oauth.html')
