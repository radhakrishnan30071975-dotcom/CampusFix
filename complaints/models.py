from django.db import models
from django.contrib.auth.models import User


# ==========================================
# MEMBER 2 - MAINTENANCE STAFF
# ==========================================

class Staff(models.Model):

    DEPARTMENT_CHOICES = [
        ('Electrical', 'Electrical'),
        ('Plumbing', 'Plumbing'),
        ('Carpentry', 'Carpentry'),
        ('IT/Network', 'IT / Network'),
        ('Housekeeping', 'Housekeeping'),
        ('General', 'General Maintenance'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )

    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    is_available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.department})"


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

    # MEMBER 2 - status tracking choices
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
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
        choices=STATUS_CHOICES,
        default='Pending'
    )

    # ==========================================
    # MEMBER 2 - STAFF ASSIGNMENT
    # ==========================================

    assigned_to = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints'
    )

    assigned_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.category + " - " + self.location


# ==========================================
# MEMBER 2 - STATUS TRACKING HISTORY
# ==========================================

class StatusLog(models.Model):

    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='status_logs'
    )

    old_status = models.CharField(max_length=30)

    new_status = models.CharField(max_length=30)

    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    remarks = models.TextField(blank=True)

    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"Complaint #{self.complaint_id}: {self.old_status} -> {self.new_status}"


class Feedback(models.Model):

    complaint = models.OneToOneField(
        Complaint,
        on_delete=models.CASCADE,
        related_name='feedback'
    )

    rating = models.IntegerField(
        choices=[
            (1, '1 - Very Poor'),
            (2, '2 - Poor'),
            (3, '3 - Average'),
            (4, '4 - Good'),
            (5, '5 - Excellent'),
        ]
    )

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.complaint} - {self.rating}/5"
