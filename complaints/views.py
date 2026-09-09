from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Complaint
from .forms import ComplaintForm


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