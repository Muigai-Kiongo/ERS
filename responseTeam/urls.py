from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard, name='staff_dashboard'),
    path('fire/', views.fireDepartment, name='fire_department'),
    path('health/', views.healthDepartment, name='health_department'),
    path('security/', views.securityDepartment, name='security_department'),
    path('disaster/', views.disasterDepartment, name='disaster_department'),
    path('incidents/<int:pk>/', views.incidents_detail, name='incidents_detail'),
    path('emergency-contacts/', views.emergency_contacts_list, name='emergency_contacts_list'),
    path('emergency-contacts/create/', views.emergency_contacts_create, name='emergency_contacts_create'),
    path('emergency-contacts/update/<int:pk>/', views.emergency_contacts_update, name='emergency_contacts_update'),
    path('emergency-contacts/delete/<int:pk>/', views.emergency_contacts_delete, name='emergency_contacts_delete'),
    path('response/report/overview/', views.reports_view, name = 'all_reports-overview'),
    path('reports/download/<str:report_type>/', views.download_report, name='all_download_report'),
]





