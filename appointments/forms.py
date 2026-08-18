from django import forms
from accounts.forms import BootstrapFormMixin
from .models import Appointment, MedicalRecord, LabResult


class AppointmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'placeholder': "Shikoyat yoki murojaat sababi..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        from datetime import date as date_cls
        if date and date < date_cls.today():
            raise forms.ValidationError("O'tmishdagi sanaga yozilib bo'lmaydi.")
        return cleaned_data


class MedicalRecordForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'prescription', 'notes']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'prescription': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()


class LabResultForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['title', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap_classes()
