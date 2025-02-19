from django import forms
from .models import Emergency, EmergencyType, ResponseTeam

class EmergencyReportForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ['emergency_type', 'description', 'assigned_teams']
        widgets = {
            'assigned_teams': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'emergency_type': 'Type of Emergency',
            'description': 'Description of the Emergency',
            'assigned_teams': 'Assign Response Teams',
        }
        help_texts = {
            'description': 'Provide a detailed description of the emergency.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emergency_type'].queryset = EmergencyType.objects.all()
        self.fields['assigned_teams'].queryset = ResponseTeam.objects.filter(available=True)