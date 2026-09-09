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
]