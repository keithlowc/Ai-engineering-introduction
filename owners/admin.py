from django.contrib import admin
from .models import PropertyOwner, InteractionLog


@admin.register(PropertyOwner)
class PropertyOwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'company_name', 'overall_rating', 'is_active', 'updated_at']
    list_filter = ['is_active', 'overall_rating', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'company_name', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone', 'company_name')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Ratings', {
            'fields': ('reliability_rating', 'communication_rating', 'maintenance_rating', 'overall_rating')
        }),
        ('Additional Info', {
            'fields': ('notes', 'last_contacted', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InteractionLog)
class InteractionLogAdmin(admin.ModelAdmin):
    list_display = ['owner', 'interaction_type', 'subject', 'interaction_date']
    list_filter = ['interaction_type', 'interaction_date']
    search_fields = ['owner__name', 'subject', 'notes']
    readonly_fields = ['interaction_date']
    
    fieldsets = (
        ('Interaction Details', {
            'fields': ('owner', 'interaction_type', 'subject')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamp', {
            'fields': ('interaction_date',),
            'classes': ('collapse',)
        }),
    )
