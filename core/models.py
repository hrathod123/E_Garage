from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Added avatar and phone from current code
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('provider', 'Service Provider'),
        ('customer', 'Customer'),
    )
    # Merged role: kept choices from current, increased length for safety
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "Categories" # This fixes the sidebar UI

    def __str__(self):
        return self.name
    
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100) # e.g., Car Wash, Engine Repair
    description = models.TextField()

    def __str__(self):
        return self.name

class Service(models.Model):
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    provider = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='services',
        limit_choices_to={'role': 'provider'}
    )
    # Using ServiceCategory to keep your current logic intact
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    estimated_time = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} by {self.provider.username}"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    # Kept your specific status choices for data integrity
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)


    class Meta:
        verbose_name_plural = "Bookings"
        
    def __str__(self):
        return f"{self.customer.username} - {self.service.title} ({self.status})"

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    garage = models.ForeignKey(User, on_delete=models.CASCADE, related_name='garage_reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)]) 
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.garage.username} - {self.rating} Stars"