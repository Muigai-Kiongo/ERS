from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from sos.models import Emergency, EmergencyType, EmergencyContacts, AidTip
from sos.forms import EmergencyContactsForm, AidTipForm, AssignResponseTeamForm, ReportForm
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.utils import timezone
from django.contrib import messages


# Custom decorator to check if the user is a staff member
def staff_member_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_staff)(view_func)
    return decorated_view_func

@staff_member_required
def dashboard(request):
    incidents = Emergency.objects.all()
    context = {
        'incidents': incidents,
    }
    return render(request, 'dashboard.html', context)

@staff_member_required
def fireDepartment(request):
    fire_type = get_object_or_404(EmergencyType, name='Fire')  # Get the EmergencyType instance for 'Fire'
    incidents = Emergency.objects.filter(emergency_type=fire_type)
    tips = AidTip.objects.filter(emergency_type=fire_type)  # Use the fire_type instance
    
    if request.method == 'POST':
        form = AidTipForm(request.POST)
        if form.is_valid():
            aid_tip = form.save(commit=False)  # Do not save to the database yet
            aid_tip.emergency_type = fire_type  # Set the emergency type
            aid_tip.save()  # Now save the instance
            return redirect('fire_department')
    else:
        form = AidTipForm()  # No initial data needed since emergency_type is set in the view
    
    context = {
        'incidents': incidents,
        'tips': tips,
        'form': form,
    }
    return render(request, 'firedepartment/fire.html', context)

@staff_member_required
def healthDepartment(request):
    medical_type = get_object_or_404(EmergencyType, name='Medical')  # Get the EmergencyType instance for 'Medical'
    incidents = Emergency.objects.filter(emergency_type=medical_type)
    tips = AidTip.objects.filter(emergency_type=medical_type)  # Use the medical_type instance
    
    if request.method == 'POST':
        form = AidTipForm(request.POST)
        if form.is_valid():
            aid_tip = form.save(commit=False)  # Do not save to the database yet
            aid_tip.emergency_type = medical_type  # Set the emergency type
            aid_tip.save()  # Now save the instance
            return redirect('health_department')
    else:
        form = AidTipForm()  # No initial data needed since emergency_type is set in the view
    
    context = {
        'incidents': incidents,
        'tips': tips,
        'form': form,
    }
    return render(request, 'healthdepartment/health.html', context)

@staff_member_required
def securityDepartment(request):
    security_type = get_object_or_404(EmergencyType, name='Security')  # Get the EmergencyType instance for 'Security'
    incidents = Emergency.objects.filter(emergency_type=security_type)
    tips = AidTip.objects.filter(emergency_type=security_type)  # Use the security_type instance
    
    if request.method == 'POST':
        form = AidTipForm(request.POST)
        if form.is_valid():
            aid_tip = form.save(commit=False)  # Do not save to the database yet
            aid_tip.emergency_type = security_type  # Set the emergency type
            aid_tip.save()  # Now save the instance
            return redirect('security_department')
    else:
        form = AidTipForm()  # No initial data needed since emergency_type is set in the view
    
    context = {
        'incidents': incidents,
        'tips': tips,
        'form': form,
    }
    return render(request, 'securitydepartment/security.html', context)

@staff_member_required
def disasterDepartment(request):
    rescue_type = get_object_or_404(EmergencyType, name='Rescue')  # Get the EmergencyType instance for 'Rescue'
    incidents = Emergency.objects.filter(emergency_type=rescue_type)
    tips = AidTip.objects.filter(emergency_type=rescue_type)  # Filter tips by the rescue type

    if request.method == 'POST':
        form = AidTipForm(request.POST)
        if form.is_valid():
            aid_tip = form.save(commit=False)  # Do not save to the database yet
            aid_tip.emergency_type = rescue_type  # Set the emergency type
            aid_tip.save()  # Now save the instance
            return redirect('disaster_department')  # Redirect after saving
    else:
        form = AidTipForm()  # No initial data needed since emergency_type is set in the view

    context = {
        'incidents': incidents,
        'tips': tips,
        'form': form,
    }
    return render(request, 'disasterdepartment/disaster.html', context)


@staff_member_required
def incidents_detail(request, pk):
    incident = get_object_or_404(Emergency, pk=pk)

    if request.method == 'POST':
        # Handle response team assignment
        if 'assign_team' in request.POST:
            assign_form = AssignResponseTeamForm(request.POST)
            if assign_form.is_valid():
                response_team = assign_form.cleaned_data['response_team']
                incident.assigned_team = response_team  # Make sure this is the team object, not just name
                incident.save()
                messages.success(request, 'Team assigned successfully!')
                return redirect('incidents_detail', pk=incident.pk)

        # Handle status update
        if 'status' in request.POST:
            new_status = request.POST.get('status')
            incident.status = new_status
            incident.save()
            messages.success(request, 'Status updated successfully!')
            return redirect('incidents_detail', pk=incident.pk)
    else:
        assign_form = AssignResponseTeamForm()

    context = {
        'incident': incident,
        'assign_form': assign_form,
    }
    return render(request, 'detail.html', context)



@staff_member_required
def emergency_contacts_list(request):
    contacts = EmergencyContacts.objects.all()
    return render(request, 'emergency_contact/contact_list.html', {'contacts': contacts})

@staff_member_required
def emergency_contacts_create(request):
    if request.method == 'POST':
        form = EmergencyContactsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('emergency_contacts_list')
    else:
        form = EmergencyContactsForm()
    return render(request, 'emergency_contact/create_contact.html', {'form': form})

@staff_member_required
def emergency_contacts_update(request, pk):
    contact = get_object_or_404(EmergencyContacts, pk=pk)
    if request.method == 'POST':
        form = EmergencyContactsForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('emergency_contacts_list')
    else:
        form = EmergencyContactsForm(instance=contact)
    return render(request, 'emergency_contact/contact_update.html', {'form': form})

@staff_member_required
def emergency_contacts_delete(request, pk):
    contact = get_object_or_404(EmergencyContacts, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('emergency_contacts_list')
    return render(request, 'emergency_contact/contact_delete.html', {'contact': contact})

@staff_member_required
def reports_view(request):
    report_html = None
    report_type = None

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            emergencies = get_emergencies(report_type)  
            report_html = render_to_string(f'report_generation/{report_type}_report.html', {'emergencies': emergencies})
    else:
        form = ReportForm()

    return render(request, 'report_generation/reports_overview.html', {
        'form': form,
        'report_html': report_html,
        'report_type': report_type,
    })

def get_emergencies(report_type):
    now = timezone.now()
    if report_type == 'weekly':
        week_start = now - timezone.timedelta(days=7)
        return Emergency.objects.filter(reported_at__gte=week_start)
    elif report_type == 'monthly':
        month_start = now.replace(day=1)
        return Emergency.objects.filter(reported_at__gte=month_start)
    elif report_type == 'yearly':
        year_start = now.replace(month=1, day=1)
        return Emergency.objects.filter(reported_at__gte=year_start)
    return Emergency.objects.none()  # Return an empty queryset for invalid report types

def generate_pdf_response(html_string, filename):
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@staff_member_required
def download_report(request, report_type):
    emergencies = get_emergencies(report_type)
    html_string = render_to_string(f'report_generation/{report_type}_report.html', {'emergencies': emergencies})
    return generate_pdf_response(html_string, f'{report_type}_report.pdf')