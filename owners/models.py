from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class PropertyOwner(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    
    # Rating fields
    reliability_rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication_rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    maintenance_rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    overall_rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contacted = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Property Owner'
        verbose_name_plural = 'Property Owners'

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        ratings = [self.reliability_rating, self.communication_rating, self.maintenance_rating]
        return round(sum(ratings) / len(ratings), 2)


class InteractionLog(models.Model):
    INTERACTION_TYPE_CHOICES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'In-Person Meeting'),
        ('text', 'Text Message'),
        ('other', 'Other'),
    ]

    owner = models.ForeignKey(PropertyOwner, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE_CHOICES)
    subject = models.CharField(max_length=255)
    notes = models.TextField()
    interaction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-interaction_date']
        verbose_name = 'Interaction Log'
        verbose_name_plural = 'Interaction Logs'

    def __str__(self):
        return f"{self.owner.name} - {self.interaction_type} on {self.interaction_date.date()}"
