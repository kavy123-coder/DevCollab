from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import postViewset,commentViewset,tagViewset
router = DefaultRouter()
router.register('posts',postViewset)
router.register('tags',tagViewset)
router.register('comments',commentViewset)

urlpatterns = [
   path('',include(router.urls)),
]
