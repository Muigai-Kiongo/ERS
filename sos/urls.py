from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stats/',views.stats, name = 'stats'),
    path('first-aid/',views.first_aid, name='aid'),
    path('incidents/',views.incidents, name='emergecies'),
    path('history/', views.history, name ='history'),
    path('emergency-contacts/', views.emergency_contacts, name='emergency_contact'),
    path('fire-reports/',views.fire_reports, name='fire-reports'),
    path('health-reports/',views.health_reports, name='health-reports'),
    path('disaster-reports/',views.disaster_reports, name='disaster-reports'),
    path('security-reports/',views.security_reports, name='security-reports'),  
    path('other-reports/', views.other_reports, name='other-reports'),  
]
