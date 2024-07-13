from django.db.models import Count, When, Case
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BookSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):
    # select_related - вибирає ОДИН об'єкт зв'язаний з книгами
    # prefer_related - вибирає ВСІ зв'язані об'єкти з книгами
    queryset = Book.objects.all().annotate(
        annotation_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        ).select_related('owner').prefetch_related('readers')
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


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    # lookup_field - робиться для зручності пошуку(для Frontand)
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        return obj


def auth(request):
    return render(request, 'oauth.html')
