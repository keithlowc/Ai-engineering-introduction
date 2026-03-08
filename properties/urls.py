from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyOwnerViewSet, PropertyViewSet, PropertyRatingViewSet

router = DefaultRouter()
router.register(r'owners', PropertyOwnerViewSet, basename='owner')
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'ratings', PropertyRatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
