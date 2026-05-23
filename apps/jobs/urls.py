from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import JobsViewset,ApplicationViewset
router = DefaultRouter()
router.register('jobs',JobsViewset)
router.register('applications',ApplicationViewset)

urlpatterns = [
   path('',include(router.urls)),
]
