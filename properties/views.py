from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import PropertyOwner, Property, PropertyRating
from .serializers import PropertyOwnerSerializer, PropertySerializer, PropertyRatingSerializer


class PropertyOwnerViewSet(viewsets.ModelViewSet):
    """ViewSet for managing property owners"""
    queryset = PropertyOwner.objects.all()
    serializer_class = PropertyOwnerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['contact_status', 'rating', 'assigned_to']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'company_name']
    ordering_fields = ['created_at', 'rating', 'first_name']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """Assign property owner to a user"""
        owner = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(id=user_id)
            owner.assigned_to = user
            owner.save()
            return Response({'status': 'Owner assigned successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Change contact status of property owner"""
        owner = self.get_object()
        status_value = request.data.get('status')
        
        valid_statuses = [choice[0] for choice in PropertyOwner.CONTACT_STATUS_CHOICES]
        if status_value not in valid_statuses:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        owner.contact_status = status_value
        owner.save()
        return Response(PropertyOwnerSerializer(owner).data)


class PropertyViewSet(viewsets.ModelViewSet):
    """ViewSet for managing properties"""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['property_type', 'owner']
    search_fields = ['address', 'city', 'state', 'owner__first_name', 'owner__last_name']
    ordering_fields = ['created_at', 'estimated_value', 'bedrooms']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        """Get average rating for a property"""
        property_obj = self.get_object()
        ratings = property_obj.ratings.all()
        
        if ratings.exists():
            avg = sum([r.rating for r in ratings]) / len(ratings)
            return Response({'average_rating': avg, 'total_ratings': len(ratings)})
        
        return Response({'average_rating': None, 'total_ratings': 0})


class PropertyRatingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing property ratings"""
    queryset = PropertyRating.objects.all()
    serializer_class = PropertyRatingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['property', 'rating']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Set the rated_by user to the current user"""
        serializer.save(rated_by=self.request.user)
