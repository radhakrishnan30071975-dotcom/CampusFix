from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Q
from django.utils import timezone

from .models import Complaint, Feedback, Staff, StatusLog
from .forms import (
    ComplaintForm,
    FeedbackForm,
    AssignStaffForm,
    StatusUpdateForm,
    StaffCreationForm,
)


@login_required
def register_complaint(request):

    if request.method == 'POST':

        form = ComplaintForm(request.POST, request.FILES)

        if form.is_valid():

            complaint = form.save(commit=False)

            complaint.user = request.user

            complaint.save()

            return redirect('my_complaints')

    else:

        form = ComplaintForm()

    return render(
        request,
        'complaints/register_complaint.html',
        {'form': form}
    )


@login_required
def my_complaints(request):

    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'complaints/my_complaints.html',
        {'complaints': complaints}
    )


@login_required
def complaint_detail(request, id):

    complaint = get_object_or_404(
        Complaint,
        id=id,
        user=request.user
    )

    return render(
        request,
        'complaints/complaint_detail.html',
        {'complaint': complaint}
    )


@login_required
def edit_complaint(request, id):

    complaint = get_object_or_404(
        Complaint,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        form = ComplaintForm(
            request.POST,
            request.FILES,
            instance=complaint
        )

        if form.is_valid():

            form.save()

            return redirect(
                'complaint_detail',
                id=complaint.id
            )

    else:

        form = ComplaintForm(instance=complaint)

    return render(
        request,
        'complaints/edit_complaint.html',
        {'form': form}
    )


@login_required
def delete_complaint(request, id):

    complaint = get_object_or_404(
        Complaint,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        complaint.delete()

        return redirect('my_complaints')

    return render(
        request,
        'complaints/delete_complaint.html',
        {'complaint': complaint}
    )


# ==========================================
# MEMBER 3 - DASHBOARD
# ==========================================

@login_required
def dashboard(request):

    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by('-created_at')

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '')
    category = request.GET.get('category', '')

    if search:
        complaints = complaints.filter(
            Q(description__icontains=search) |
            Q(location__icontains=search) |
            Q(category__icontains=search)
        )

    if status:
        complaints = complaints.filter(status=status)

    if category:
        complaints = complaints.filter(category=category)

    all_complaints = Complaint.objects.filter(user=request.user)

    total = all_complaints.count()
    pending = all_complaints.filter(status='Pending').count()
    in_progress = all_complaints.filter(status='In Progress').count()
    resolved = all_complaints.filter(status='Resolved').count()

    feedbacks = Feedback.objects.filter(
        complaint__user=request.user
    )

    average_rating = feedbacks.aggregate(
        Avg('rating')
    )['rating__avg']

    context = {
        'complaints': complaints,
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved,
        'average_rating': average_rating,
        'search': search,
        'selected_status': status,
        'selected_category': category,
        'categories': Complaint.CATEGORY_CHOICES,
    }

    return render(
        request,
        'complaints/dashboard.html',
        context
    )


# ==========================================
# MEMBER 3 - FEEDBACK
# ==========================================

@login_required
def feedback(request, id):

    complaint = get_object_or_404(
        Complaint,
        id=id,
        user=request.user
    )

    if complaint.status != 'Resolved':
        return redirect(
            'complaint_detail',
            id=complaint.id
        )

    existing_feedback = Feedback.objects.filter(
        complaint=complaint
    ).first()

    if request.method == 'POST':

        form = FeedbackForm(
            request.POST,
            instance=existing_feedback
        )

        if form.is_valid():

            feedback_obj = form.save(commit=False)
            feedback_obj.complaint = complaint
            feedback_obj.save()

            return redirect('dashboard')

    else:

        form = FeedbackForm(
            instance=existing_feedback
        )

    return render(
        request,
        'complaints/feedback.html',
        {
            'form': form,
            'complaint': complaint
        }
    )


# ==========================================
# MEMBER 2 - STAFF ASSIGNMENT & STATUS TRACKING
# ==========================================

def staff_required(view_func):
    """
    Restricts a view to users who have a linked Staff (maintenance) profile.
    Regular complaint-registering users are redirected back to their own page.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):

        if not hasattr(request.user, 'staff_profile'):
            messages.error(
                request,
                "You are not authorized to access the staff area."
            )
            return redirect('my_complaints')

        return view_func(request, *args, **kwargs)

    return wrapper


@staff_member_required
def manage_complaints(request):
    """
    Admin/manager view: lists every complaint in the system so it can be
    assigned to a maintenance staff member. Supports filtering by status
    and by assignment state.
    """

    complaints = Complaint.objects.all().order_by('-created_at')

    status = request.GET.get('status', '')
    assignment = request.GET.get('assignment', '')

    if status:
        complaints = complaints.filter(status=status)

    if assignment == 'unassigned':
        complaints = complaints.filter(assigned_to__isnull=True)
    elif assignment == 'assigned':
        complaints = complaints.filter(assigned_to__isnull=False)

    context = {
        'complaints': complaints,
        'selected_status': status,
        'selected_assignment': assignment,
        'status_choices': Complaint.STATUS_CHOICES,
    }

    return render(
        request,
        'complaints/manage_complaints.html',
        context
    )


@staff_member_required
def assign_complaint(request, id):
    """Admin/manager assigns (or re-assigns) a complaint to a maintenance staff member."""

    complaint = get_object_or_404(Complaint, id=id)
    old_status = complaint.status

    if request.method == 'POST':

        form = AssignStaffForm(request.POST, instance=complaint)

        if form.is_valid():

            updated = form.save(commit=False)

            if updated.assigned_to:
                updated.assigned_at = timezone.now()

                # Move a freshly assigned complaint out of the Pending queue.
                if updated.status == 'Pending':
                    updated.status = 'In Progress'
            else:
                updated.assigned_at = None

            updated.save()

            if updated.status != old_status or updated.assigned_to:
                StatusLog.objects.create(
                    complaint=updated,
                    old_status=old_status,
                    new_status=updated.status,
                    changed_by=request.user,
                    remarks=(
                        f"Assigned to {updated.assigned_to}"
                        if updated.assigned_to
                        else "Staff assignment removed"
                    )
                )

            messages.success(
                request,
                f"Complaint #{updated.id} has been updated."
            )

            return redirect('manage_complaints')

    else:
        form = AssignStaffForm(instance=complaint)

    return render(
        request,
        'complaints/assign_complaint.html',
        {
            'form': form,
            'complaint': complaint,
        }
    )


@staff_member_required
def staff_list(request):
    """Admin/manager view: list of maintenance staff and a form to add new ones."""

    staff_members = Staff.objects.all().order_by('department', 'user__username')

    if request.method == 'POST':

        form = StaffCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Staff member added successfully.")
            return redirect('staff_list')

    else:
        form = StaffCreationForm()

    return render(
        request,
        'complaints/staff_list.html',
        {
            'staff_members': staff_members,
            'form': form,
        }
    )


@staff_required
def staff_dashboard(request):
    """Maintenance staff view: shows complaints assigned to the logged-in staff member."""

    staff_profile = request.user.staff_profile

    complaints = Complaint.objects.filter(
        assigned_to=staff_profile
    ).order_by('-assigned_at')

    status = request.GET.get('status', '')

    if status:
        complaints = complaints.filter(status=status)

    base_qs = Complaint.objects.filter(assigned_to=staff_profile)

    context = {
        'complaints': complaints,
        'staff_profile': staff_profile,
        'total_assigned': base_qs.count(),
        'pending': base_qs.filter(status='Pending').count(),
        'in_progress': base_qs.filter(status='In Progress').count(),
        'resolved': base_qs.filter(status='Resolved').count(),
        'selected_status': status,
    }

    return render(
        request,
        'complaints/staff_dashboard.html',
        context
    )


@staff_required
def update_status(request, id):
    """Maintenance staff updates the status of a complaint assigned to them."""

    staff_profile = request.user.staff_profile

    complaint = get_object_or_404(
        Complaint,
        id=id,
        assigned_to=staff_profile
    )

    old_status = complaint.status

    if request.method == 'POST':

        form = StatusUpdateForm(request.POST, instance=complaint)

        if form.is_valid():

            updated = form.save()
            remarks = form.cleaned_data.get('remarks', '')

            if updated.status != old_status:

                StatusLog.objects.create(
                    complaint=updated,
                    old_status=old_status,
                    new_status=updated.status,
                    changed_by=request.user,
                    remarks=remarks
                )

                messages.success(
                    request,
                    f"Status updated to '{updated.status}'."
                )

            else:
                messages.info(request, "Status unchanged.")

            return redirect('staff_dashboard')

    else:
        form = StatusUpdateForm(instance=complaint)

    return render(
        request,
        'complaints/update_status.html',
        {
            'form': form,
            'complaint': complaint,
        }
    )


@login_required
def status_history(request, id):
    """
    Shows the full assignment/status timeline for a complaint.
    Visible to the complaint's owner, the assigned staff member, or an admin.
    """

    complaint = get_object_or_404(Complaint, id=id)

    is_owner = complaint.user == request.user
    is_assigned_staff = (
        hasattr(request.user, 'staff_profile')
        and complaint.assigned_to_id == request.user.staff_profile.id
    )

    if not (is_owner or is_assigned_staff or request.user.is_staff):
        raise PermissionDenied

    logs = complaint.status_logs.all()

    return render(
        request,
        'complaints/status_history.html',
        {
            'complaint': complaint,
            'logs': logs,
        }
    )
