from django.contrib import admin
from .models import PropertyOwner, Property, PropertyRating

@admin.register(PropertyOwner)
class PropertyOwnerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'contact_status', 'rating', 'created_at']
    list_filter = ['contact_status', 'created_at', 'rating']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company_name')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('CRM Information', {
            'fields': ('contact_status', 'rating', 'assigned_to', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['address', 'city', 'property_type', 'owner', 'estimated_value', 'created_at']
    list_filter = ['property_type', 'created_at', 'year_built']
    search_fields = ['address', 'city', 'owner__first_name', 'owner__last_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Owner Information', {
            'fields': ('owner',)
        }),
        ('Property Details', {
            'fields': ('property_type', 'address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Property Specifications', {
            'fields': ('square_feet', 'bedrooms', 'bathrooms', 'year_built')
        }),
        ('Valuation', {
            'fields': ('estimated_value', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PropertyRating)
class PropertyRatingAdmin(admin.ModelAdmin):
    list_display = ['property', 'rating', 'rated_by', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['property__address', 'comment']
    readonly_fields = ['created_at', 'updated_at']
