from django.shortcuts import render
from rest_framework import viewsets
from .serializer import postserializer,tagserializer,commentserializer
from .models import Post,Tag,Comment
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.users.permissons import IsOwnerOrReadOnly
# Create your views here.
class postViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = postserializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['tags']
    search_fields = ['title', 'content','author__username']
    pagination_class = LimitOffsetPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class tagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = tagserializer
    authentication_classes = [JWTAuthentication]
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
    
    

class commentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = commentserializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)