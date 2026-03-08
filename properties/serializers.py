from rest_framework import serializers
from .models import PropertyOwner, Property, PropertyRating

class PropertyRatingSerializer(serializers.ModelSerializer):
    rated_by_name = serializers.CharField(source='rated_by.get_full_name', read_only=True)
    
    class Meta:
        model = PropertyRating
        fields = ['id', 'rating', 'comment', 'rated_by', 'rated_by_name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PropertySerializer(serializers.ModelSerializer):
    ratings = PropertyRatingSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = ['id', 'owner', 'property_type', 'address', 'city', 'state', 'zip_code', 'country',
                  'square_feet', 'bedrooms', 'bathrooms', 'year_built', 'estimated_value', 'description',
                  'ratings', 'average_rating', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return sum([r.rating for r in ratings]) / len(ratings)
        return None


class PropertyOwnerSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = PropertyOwner
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'company_name',
                  'address', 'city', 'state', 'zip_code', 'country',
                  'contact_status', 'rating', 'assigned_to', 'assigned_to_name', 'notes',
                  'properties', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
