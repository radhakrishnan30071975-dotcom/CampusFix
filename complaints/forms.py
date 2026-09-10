from django import forms
from .models import Complaint, Feedback, Staff


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint

        fields = [
            'category',
            'location',
            'description',
            'image'
        ]


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = [
            'rating',
            'comment'
        ]

        widgets = {
            'rating': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Write your feedback...'
                }
            ),
        }


# ==========================================
# MEMBER 2 - STAFF ASSIGNMENT & STATUS TRACKING
# ==========================================

class AssignStaffForm(forms.ModelForm):
    """Used by admin/managers to assign a complaint to a maintenance staff member."""

    class Meta:
        model = Complaint
        fields = ['assigned_to']
        widgets = {
            'assigned_to': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = Staff.objects.all()
        self.fields['assigned_to'].empty_label = "-- Select Staff Member --"


class StatusUpdateForm(forms.ModelForm):
    """Used by maintenance staff to update the status of a complaint assigned to them."""

    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add remarks about this update (optional)'
            }
        )
    )

    class Meta:
        model = Complaint
        fields = ['status']
        widgets = {
            'status': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }


class StaffCreationForm(forms.ModelForm):
    """Used by admin to create a new maintenance staff record for an existing user."""

    class Meta:
        model = Staff
        fields = ['user', 'department', 'phone', 'is_available']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact number'}),
        }
