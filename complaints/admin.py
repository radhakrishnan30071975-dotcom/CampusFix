from django.contrib import admin
from .models import Complaint, Staff, StatusLog, Feedback


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'location', 'status', 'user', 'assigned_to', 'created_at')
    list_filter = ('status', 'category', 'assigned_to')
    search_fields = ('location', 'description', 'user__username')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'phone', 'is_available')
    list_filter = ('department', 'is_available')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'old_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('old_status', 'new_status')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'rating', 'created_at')
