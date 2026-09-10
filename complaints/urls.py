from django.urls import path
from . import views


urlpatterns = [

    path(
        'register/',
        views.register_complaint,
        name='register_complaint'
    ),

    path(
        'my/',
        views.my_complaints,
        name='my_complaints'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # ==========================================
    # MEMBER 2 - STAFF ASSIGNMENT & STATUS TRACKING
    # ==========================================

    path(
        'manage/',
        views.manage_complaints,
        name='manage_complaints'
    ),

    path(
        'manage/<int:id>/assign/',
        views.assign_complaint,
        name='assign_complaint'
    ),

    path(
        'staff/',
        views.staff_list,
        name='staff_list'
    ),

    path(
        'staff/dashboard/',
        views.staff_dashboard,
        name='staff_dashboard'
    ),

    path(
        'staff/<int:id>/update-status/',
        views.update_status,
        name='update_status'
    ),

    path(
        '<int:id>/',
        views.complaint_detail,
        name='complaint_detail'
    ),

    path(
        '<int:id>/edit/',
        views.edit_complaint,
        name='edit_complaint'
    ),

    path(
        '<int:id>/delete/',
        views.delete_complaint,
        name='delete_complaint'
    ),

    path(
        '<int:id>/feedback/',
        views.feedback,
        name='feedback'
    ),

    path(
        '<int:id>/history/',
        views.status_history,
        name='status_history'
    ),
]
