from django.contrib import admin
from django.contrib.auth.models import User, Group  # Import User and Group models
from django.urls import path
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Emergency, EmergencyType, ResponseTeam, EmergencyContacts, PersonalEmergencyContacts, AidTip
from .forms import ReportForm  # You'll need to create this form

class CustomAdminSite(admin.AdminSite):
    site_header = "Emergency Management System"
    site_title = "Emergency Management"
    index_title = "Welcome to Emergency Management System"

custom_admin_site = CustomAdminSite(name='custom_admin')

class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'emergency_type', 'reported_by', 'description', 'reported_at', 'status')
    list_filter = ('status', 'emergency_type', 'reported_by')
    search_fields = ('description', 'reported_by__username')
    change_list_template = 'admin/emergency/emergency_change_list.html'  # Custom template for the change list

    def reports_view(self, request):
        report_html = None
        report_type = None

        if request.method == 'POST':
            form = ReportForm(request.POST)
            if form.is_valid():
                report_type = form.cleaned_data['report_type']
                emergencies = self.get_emergencies(report_type)
                report_html = render_to_string(f'reports/{report_type}_report.html', {'emergencies': emergencies})
        else:
            form = ReportForm()

        context = {
            'form': form,
            'report_html': report_html,
            'report_type': report_type,
            **self.admin_site.each_context(request),  # Include additional context
        }
        return render(request, 'admin/reports.html', context)

    def get_emergencies(self, report_type):
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
        return Emergency.objects.none()

    def generate_pdf_response(self, html_string, filename):
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    def download_report(self, request, report_type):
        emergencies = self.get_emergencies(report_type)
        html_string = render_to_string(f'reports/{report_type}_report.html', {'emergencies': emergencies})
        return self.generate_pdf_response(html_string, f'{report_type}_report.pdf')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('reports/', self.admin_site.admin_view(self.reports_view), name='reports_view'),
            path('reports/download/<str:report_type>/', self.admin_site.admin_view(self.download_report), name='download_report'),
        ]
        return custom_urls + urls

# Register your models with the custom admin site
custom_admin_site.register(Emergency, EmergencyAdmin)
custom_admin_site.register(EmergencyType)
custom_admin_site.register(ResponseTeam)
custom_admin_site.register(EmergencyContacts)
custom_admin_site.register(PersonalEmergencyContacts)
custom_admin_site.register(AidTip)

# Register the User and Group models with the custom admin site
custom_admin_site.register(User)
custom_admin_site.register(Group)