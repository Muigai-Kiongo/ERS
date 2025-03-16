from django import forms
from .models import Emergency, EmergencyType, ResponseTeam, EmergencyContacts, PersonalEmergencyContacts, AidTip

class EmergencyReportForm(forms.ModelForm):
    class Meta:
        model = Emergency
        fields = ['emergency_type', 'description', 'location']  # Removed 'assigned_teams'
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide a detailed description of the emergency.', 'rows': 3}),
        }
        labels = {
            'emergency_type': 'Type of Emergency',
            'description': 'Description of the Emergency',
            'location': 'Emergency Location',
        }
        help_texts = {
            'description': 'Provide a detailed description of the emergency.',
            'location': 'Select the location of the emergency from the dropdown.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emergency_type'].queryset = EmergencyType.objects.all()
        self.fields['location'].choices = Emergency.LOCATION_CHOICES

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("This field is required.")
        return description

class EmergencyContactsForm(forms.ModelForm):
    class Meta:
        model = EmergencyContacts
        fields = ['name', 'phone', 'email', 'emergency_type']  # Updated field name
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'emergency_type': forms.Select(attrs={'class': 'form-control'}),  # Updated field name
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

class PersonalEmergencyContactsForm(forms.ModelForm):
    class Meta:
        model = PersonalEmergencyContacts
        fields = ['name', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone


class AidTipForm(forms.ModelForm):
    class Meta:
        model = AidTip
        fields = ['tip']  # Only include the tip field

    def __init__(self, *args, **kwargs):
        super(AidTipForm, self).__init__(*args, **kwargs)

class ReportForm(forms.Form):
    REPORT_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    report_type = forms.ChoiceField(choices=REPORT_CHOICES, label="Select Report Type")

class AssignResponseTeamForm(forms.Form):
    response_team = forms.ModelChoiceField(
        queryset=ResponseTeam.objects.all(),
        empty_label="Select a Response Team",
        help_text="Choose an existing response team to assign to this incident."
    )
