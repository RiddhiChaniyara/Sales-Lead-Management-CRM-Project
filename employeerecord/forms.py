# forms.py
from django import forms
from ersapp.models import Lead, Employees,LeaveRequest

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'contact_number', 'city', 'state', 'assigned_user']

    # Add additional validations if needed
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if len(contact_number) != 10 or not contact_number.isdigit():
            raise forms.ValidationError('Contact number must be exactly 10 digits.')
        return contact_number
    
class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        exclude = ['user', 'status', 'created_at']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
            'from_time': forms.TimeInput(attrs={'type': 'time'}),
            'to_time': forms.TimeInput(attrs={'type': 'time'}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')

        if from_date and to_date and from_date > to_date:
            raise forms.ValidationError("From date cannot be later than to date.")
        
        return cleaned_data
