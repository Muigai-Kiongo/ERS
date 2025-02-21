from django.shortcuts import render, redirect
from .forms import EmergencyReportForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context ={
        'title': 'Home',

    }
    return render(request, 'index.html', context)

def emergency_contacts(request):
    
    context ={

    }
    return render(request, 'contact/contact.html', context)

def first_aid(request):
    context ={

    }
    return render(request, 'aid/aid.html', context)    

    
@login_required
def stats(request):
    context={
        
    }

    return render(request, 'stats/stats.html', context)

@login_required
def history(request):
    context ={

    }
    return render(request, 'history/history.html', context)



@login_required
def incidents(request):
    context ={

    }
    return render(request, 'incidents/incidents.html', context)


@login_required
def fire_reports(request):
    if request.method == 'POST':
        form = EmergencyReportForm(request.POST)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.reported_by = request.user  # Set the user who reported the emergency
            emergency.save()  # Save the emergency instance
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('emergency_report_success')  # Redirect to a success page
    else:
        form = EmergencyReportForm()
    context ={
        'form': form,

    }
    return render(request, 'reports/fire-reports.html', context)


@login_required
def health_reports(request):
    if request.method == 'POST':
        form = EmergencyReportForm(request.POST)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.reported_by = request.user  # Set the user who reported the emergency
            emergency.save()  # Save the emergency instance
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('emergency_report_success')  # Redirect to a success page
    else:
        form = EmergencyReportForm()
    context ={
        'form': form,

    }
    return render(request, 'reports/health-reports.html', context)


@login_required
def disaster_reports(request):
    if request.method == 'POST':
        form = EmergencyReportForm(request.POST)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.reported_by = request.user  # Set the user who reported the emergency
            emergency.save()  # Save the emergency instance
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('emergency_report_success')  # Redirect to a success page
    else:
        form = EmergencyReportForm()
    context ={
        'form': form,

    }
    return render(request, 'reports/disaster-reports.html', context)


@login_required
def security_reports(request):
    if request.method == 'POST':
        form = EmergencyReportForm(request.POST)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.reported_by = request.user  # Set the user who reported the emergency
            emergency.save()  # Save the emergency instance
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('emergency_report_success')  # Redirect to a success page
    else:
        form = EmergencyReportForm()
    context ={
        'form': form,

    }
    return render(request, 'reports/security-reports.html', context)


@login_required
def other_reports(request):
    if request.method == 'POST':
        form = EmergencyReportForm(request.POST)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.reported_by = request.user  # Set the user who reported the emergency
            emergency.save()  # Save the emergency instance
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('emergency_report_success')  # Redirect to a success page
    else:
        form = EmergencyReportForm()
    context ={
        'form': form,

    }
    return render(request, 'reports/other.html', context)

