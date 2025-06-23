from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stats/',views.stats, name = 'stats'),
    path('first-aid/',views.first_aid, name='aid'),
    path('incidents/',views.incidents, name='emergecies'),
    path('history/', views.history, name ='history'),
    path('emergency-contacts/', views.emergency_contacts, name='personal_emergency_contact'),
    path('emergency-contacts/create/', views.emergency_contacts_create, name='personal_emergency_contacts_create'),
    path('emergency-contacts/update/<int:pk>/', views.emergency_contacts_update, name='personal_emergency_contacts_update'),
    path('emergency-contacts/delete/<int:pk>/', views.emergency_contacts_delete, name='personal_emergency_contacts_delete'),
    path('report/', views.report, name='report'),  
    path('report/overview/', views.reports_view, name = 'reports-overview'),
    path('reports/download/<str:report_type>/', views.download_report, name='download_report'),
    path('donations/', views.donations, name='donate')
    
]
