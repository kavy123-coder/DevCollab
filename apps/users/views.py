from django.shortcuts import render
from rest_framework import viewsets
from .serializer import skillserializer,userprofileserializer
from .models import Skill,Userprofile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from .permissons import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    queryset = Userprofile.objects.all()
    serializer_class = userprofileserializer
    filter_backends = [DjangoFilterBackend,SearchFilter]
    search_fields = ['user__username']
    pagination_class = LimitOffsetPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    
    def perform_create(self, serializer):
        if Userprofile.objects.filter(user=self.request.user).exists():
         raise ValidationError("Profile already exists")
        serializer.save(user=self.request.user)

class SkillViewset(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Skill.objects.all()
    serializer_class = skillserializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]