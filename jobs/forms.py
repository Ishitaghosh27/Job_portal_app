from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Senior Python Developer'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the role, requirements, and responsibilities...', 'rows': 6}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Mumbai, India'}),
            'salary': forms.TextInput(attrs={'placeholder': 'e.g. ₹8,00,000 - ₹12,00,000 per annum'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'placeholder': 'Tell the employer why you are a great fit for this role...', 'rows': 5}),
        }
