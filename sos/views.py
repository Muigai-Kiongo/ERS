from django.shortcuts import render, redirect
from .forms import EmergencyReportForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context ={
        'title': 'Home',

    }
    return render(request, 'index.html', context)


@login_required
def stats(request):

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
    return render(request, 'stats/stats.html', context)

def history(request):
    context ={

    }
    return render(request, 'history/history.html', context)

def first_aid(request):
    context ={

    }
    return render(request, 'aid/aid.html', context) 


def incidents(request):
    context ={

    }
    return render(request, 'incidents/incidents.html', context)

def fire_reports(request):
    context ={

    }
    return render(request, 'reports/fire-reports.html', context)

def health_reports(request):
    context ={

    }
    return render(request, 'reports/health-reports.html', context)

def disaster_reports(request):
    context ={

    }
    return render(request, 'reports/disaster-reports.html', context)

def security_reports(request):
    context ={

    }
    return render(request, 'reports/security-reports.html', context)


def other_reports(request):
    context ={

    }
    return render(request, 'reports/other.html', context)

def emergency_contacts(request):
    context ={

    }
    return render(request, 'contact/contact.html', context)