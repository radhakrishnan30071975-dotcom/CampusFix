from django.db import models
from django.contrib.auth.models import User


class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('Classroom', 'Classroom'),
        ('Laboratory', 'Laboratory'),
        ('Hostel', 'Hostel'),
        ('Electrical', 'Electrical'),
        ('Internet', 'Internet'),
        ('Plumbing', 'Plumbing'),
        ('Furniture', 'Furniture'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    location = models.CharField(
        max_length=200
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='complaints/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=30,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.category + " - " + self.location