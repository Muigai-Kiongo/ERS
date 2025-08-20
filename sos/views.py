from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmergencyReportForm,EmergencyContactsForm, PersonalEmergencyContactsForm, ReportForm
from django.contrib.auth.decorators import login_required
from .models import Emergency, PersonalEmergencyContacts, EmergencyContacts, AidTip
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from twilio.rest import Client
from django.db.models import Count
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.utils import timezone
import logging

# Set up logging
logger = logging.getLogger(__name__)


def index(request):

    context ={
        'title': 'Home',

    }
    return render(request, 'index.html', context)

@login_required
def emergency_contacts(request):
    contacts = PersonalEmergencyContacts.objects.all()
    sos= EmergencyContacts.objects.all()
    return render(request, 'contact/contact.html', {
        'contacts': contacts,
        'sos':sos
        })

def donations(request):
    return render(request, 'donations.html')

@login_required
def emergency_contacts_create(request):
    if request.method == 'POST':
        form = PersonalEmergencyContactsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personal_emergency_contact')
    else:
        form = PersonalEmergencyContactsForm()
    return render(request, 'contact/contact_create.html', {'form': form})

@login_required
def emergency_contacts_update(request, pk):
    contact = get_object_or_404(PersonalEmergencyContacts, pk=pk)
    if request.method == 'POST':
        form = PersonalEmergencyContactsForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('personal_emergency_contact')
    else:
        form = PersonalEmergencyContactsForm(instance=contact)
    return render(request, 'contact/contact_create.html', {'form': form})

@login_required
def emergency_contacts_delete(request, pk):
    contact = get_object_or_404(PersonalEmergencyContacts, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('personal_emergency_contact')
    return render(request, 'contact/contact_delete.html', {'contact': contact})

def first_aid(request):
    # Fetch first aid tips from the database
    tips = AidTip.objects.all()  # Adjust this if you have specific filtering criteria

    context = {
        'tips': tips,  # Pass the tips to the template
    }
    return render(request, 'aid/aid.html', context)   

    
@login_required
def stats(request):
    # Filter emergencies by the logged-in user
    user_emergencies = Emergency.objects.filter(reported_by=request.user)
    
    total_emergencies = user_emergencies.count()
    emergencies_by_status = user_emergencies.values('status').annotate(count=Count('id'))
    emergencies_by_type = user_emergencies.values('emergency_type__name').annotate(count=Count('id'))
    
    context = {
        'total_emergencies': total_emergencies,
        'emergencies_by_status': emergencies_by_status,
        'emergencies_by_type': emergencies_by_type,
    }
    return render(request, 'stats/stats.html', context)

@login_required
def history(request):
    incidents = Emergency.objects.all()
    context ={
        'incidents':incidents,

    }
    return render(request, 'history/history.html', context)



@login_required
def incidents(request):
    context ={

    }
    return render(request, 'incidents/incidents.html', context)

def staff_member_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_staff)(view_func)
    return decorated_view_func

@login_required
def report(request):
    if request.method == 'POST':
        form = EmergencyReportForm(request.POST)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.reported_by = request.user  # Set the user who reported the emergency
            emergency.save()  # Save the emergency instance
            form.save_m2m()  # Save the many-to-many relationships
            
            # Prepare email content
            subject = 'New Emergency Report Submitted'
            emergency_type = form.cleaned_data['emergency_type']
            description = form.cleaned_data['description']
            location = form.cleaned_data['location']

            # Create a cleaner message
            message = f"""
            A new emergency report has been submitted by {request.user.username}.

            Details:
            Type of Emergency: {emergency_type}
            Description: {description}
            Location: {location}

            Please review the report.
            """
            recipient_list = User.objects.filter(is_staff=True).values_list('email', flat=True)

            # Send the email
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

    else:
        form = EmergencyReportForm()

    context = {
        'form': form,
    }
    return render(request, 'reports/report.html', context)

@login_required  # Ensure the user is logged in
def reports_view(request):
    report_html = None
    report_type = None

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            emergencies = get_emergencies(report_type, request.user)  # Pass the logged-in user
            report_html = render_to_string(f'reports/{report_type}_report.html', {'emergencies': emergencies})
    else:
        form = ReportForm()

    return render(request, 'reports/reports_overview.html', {
        'form': form,
        'report_html': report_html,
        'report_type': report_type,
    })

def get_emergencies(report_type, user):
    now = timezone.now()
    if report_type == 'weekly':
        week_start = now - timezone.timedelta(days=7)
        return Emergency.objects.filter(reported_at__gte=week_start, reported_by=user)
    elif report_type == 'monthly':
        month_start = now.replace(day=1)
        return Emergency.objects.filter(reported_at__gte=month_start, reported_by=user)
    elif report_type == 'yearly':
        year_start = now.replace(month=1, day=1)
        return Emergency.objects.filter(reported_at__gte=year_start, reported_by=user)
    return Emergency.objects.none()  # Return an empty queryset for invalid report types

def generate_pdf_response(html_string, filename):
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required  # Ensure the user is logged in
def download_report(request, report_type):
    emergencies = get_emergencies(report_type, request.user)  # Pass the logged-in user
    html_string = render_to_string(f'reports/{report_type}_report.html', {'emergencies': emergencies})
    return generate_pdf_response(html_string, f'{report_type}_report.pdf')