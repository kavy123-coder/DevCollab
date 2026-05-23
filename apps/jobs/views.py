from django.shortcuts import render
from rest_framework import viewsets
from .serializer import Jobsserializer,Applicationserializer
from .models import Jobs,Application
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from apps.users.permissons import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
# Create your views here.
class JobsViewset(viewsets.ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = Jobsserializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['skill_required','location','is_remote']
    ordering_fields = ['created_at']
    pagination_class = LimitOffsetPagination
    authentication_classes =[JWTAuthentication]
    permission_classes =[IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    

    def perform_create(self, serializer): 
        try:
            profile = self.request.user.userprofile
        except:
            raise PermissionDenied("Profile does not exists.")
        
        # Sirf recruiter job post kar sakta hai
        if profile.role != 'Recruiter':
            raise PermissionDenied("YOU DONT HAI PERMISSION TO POST JOB")
        
        serializer.save(recruiter=self.request.user)
    

class ApplicationViewset(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = Applicationserializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['job','status','applicant']
    ordering_fields = ['applied_at']
    authentication_classes =[JWTAuthentication]
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = user.userprofile

        if profile.role == 'Developer':
            return Application.objects.filter(applicant=user)
        
        elif profile.role == 'Recruiter':
            return Application.objects.filter(job__recruiter=user)
        
        elif profile.role == 'Admin':
            return Application.objects.all()

    def perform_create(self, serializer):
        try:
            profile = self.request.user.userprofile
        except:
            raise PermissionDenied("Profile does not exists.")
        
        if profile.role != 'Developer':
            raise PermissionDenied("only developers can apply for the job.")
        
        serializer.save(applicant=self.request.user)
    

    
