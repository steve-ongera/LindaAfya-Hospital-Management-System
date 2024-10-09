from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class CustomUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Set the password securely
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'role', 'contact_info', 'bio']


class NonStaffForm(forms.ModelForm):
    class Meta:
        model = NonStaff
        fields = ['name', 'contact_info', 'role', 'company', 'reason_for_visit', 'exit_time']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user_name', 'dob', 'gender', 'phone', 'identification_no', 'address', 'contact_info', 'medical_history', 'bed_allocation','profile_image']


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['user_name', 'specialization', 'schedule', 'patients']


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['user', 'role', 'contact_info']


class NHIFPaymentForm(forms.ModelForm):
    class Meta:
        model = NHIFPayment
        fields = ['patient', 'nhif_number', 'payment_date', 'amount_paid', 'payment_method']

class DoctorAppointmentForm(forms.ModelForm):
    class Meta:
        model = DoctorAppointment
        fields = ['doctor', 'appointment_date', 'symptoms']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.all()
        self.fields['appointment_date'].widget.attrs['type'] = 'datetime-local'


# List of counties and coordinates (only names will be used in the form)
COUNTIES = [
    ('Muranga', 'Muranga'),
    ('Kisumu', 'Kisumu'),
    ('Mombasa', 'Mombasa'),
    ('Nairobi', 'Nairobi'),
    ('Nakuru', 'Nakuru'),
    ('Uasin Gishu', 'Uasin Gishu'),
    ('Homa Bay', 'Homa Bay'),
    ('Kilifi', 'Kilifi'),
    ('Kiambu', 'Kiambu'),
    ('Marsabit', 'Marsabit'),
    ('Baringo', 'Baringo'),
    ('Bomet', 'Bomet'),
    ('Bungoma', 'Bungoma'),
    ('Busia', 'Busia'),
    ('Elgeyo-Marakwet', 'Elgeyo-Marakwet'),
    ('Embu', 'Embu'),
    ('Garissa', 'Garissa'),
    ('Isiolo', 'Isiolo'),
    ('Kajiado', 'Kajiado'),
    ('Kakamega', 'Kakamega'),
    ('Kericho', 'Kericho'),
    ('Kirinyaga', 'Kirinyaga'),
    ('Kitui', 'Kitui'),
    ('Kwale', 'Kwale'),
    ('Laikipia', 'Laikipia'),
    ('Lamu', 'Lamu'),
    ('Machakos', 'Machakos'),
    ('Makueni', 'Makueni'),
    ('Mandera', 'Mandera'),
    ('Meru', 'Meru'),
    ('Migori', 'Migori'),
    ('Narok', 'Narok'),
    ('Nyamira', 'Nyamira'),
    ('Nyandarua', 'Nyandarua'),
    ('Nyeri', 'Nyeri'),
    ('Samburu', 'Samburu'),
    ('Siaya', 'Siaya'),
    ('Taita-Taveta', 'Taita-Taveta'),
    ('Tana River', 'Tana River'),
    ('Tharaka-Nithi', 'Tharaka-Nithi'),
    ('Trans Nzoia', 'Trans Nzoia'),
    ('Turkana', 'Turkana'),
    ('Vihiga', 'Vihiga'),
    ('Wajir', 'Wajir'),
    ('West Pokot', 'West Pokot'),
    ('Kisii', 'Kisii'),
    ('Nyamira', 'Nyamira'),
]

class TBPatientForm(forms.ModelForm):
    county = forms.ChoiceField(choices=COUNTIES)  # Restrict to county dropdown

    class Meta:
        model = TBPatient
        fields = '__all__'