from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
#from django.contrib.gis.db import models as gis_models  # For geolocation data
from django.db import models
from django.contrib.auth.models import User

class County(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class KenyaHospitalData(models.Model):
    # This will be used for both patients and doctors, and staff.
    IDENTIFICATION_CHOICES = [
        ('National ID', 'National ID'),
        ('Passport', 'Passport'),
        ('Alien ID', 'Alien ID'),
    ]

    identification_no = models.CharField(max_length=20, unique=True)
    identification_type = models.CharField(max_length=20, choices=IDENTIFICATION_CHOICES, default='National ID')
    user_name = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    nhif_no = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255)
   

    # Determine if this person is a doctor, patient, or staff
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_name} - {self.identification_no}"

    class Meta:
        verbose_name = 'Hospital User'
        verbose_name_plural = 'Hospital Users'


class Patient(models.Model):
    user_name = models.CharField(max_length=100 , null=True, blank=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    identification_no = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=15)
    medical_history = models.TextField()
    bed_allocation = models.OneToOneField('Bed', on_delete=models.SET_NULL, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default_profile.png')  # Added profile image field

    def __str__(self):
        return f"{self.user_name} {self.identification_no}"

class Doctor(models.Model):
    user_name = models.CharField(max_length=100 , null=True, blank=True)
    specialization = models.CharField(max_length=100)
    schedule = models.TextField()
    patients = models.ManyToManyField(Patient, related_name='assigned_doctors', blank=True)

    def __str__(self):
        return f"Dr. {self.user_name} - {self.specialization}"

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    contact_info = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.role}"

class Bed(models.Model):
    bed_number = models.CharField(max_length=10, unique=True)
    ward = models.CharField(max_length=50)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Bed {self.bed_number} in Ward {self.ward}"
    

class Profile(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.png')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    contact_info = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    def is_patient(self):
        return self.role == 'patient'

    def is_doctor(self):
        return self.role == 'doctor'

    def is_staff(self):
        return self.role == 'staff'

    def is_admin(self):
        return self.role == 'admin'


class NonStaff(models.Model):
    ROLE_CHOICES = [
        ('visitor', 'Visitor'),
        ('vendor', 'Vendor'),
        ('contractor', 'Contractor'),
    ]

    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company = models.CharField(max_length=100, blank=True, null=True)
    reason_for_visit = models.TextField()
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

    def is_present(self):
        return self.exit_time is None
    

class NHIFPayment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='nhif_payments')
    nhif_number = models.CharField(max_length=20)
    payment_date = models.DateField(default=timezone.now)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('MPESA', 'Mpesa'), ('Bank', 'Bank Transfer'), ('Cash', 'Cash')])

    def __str__(self):
        return f"{self.patient.user_name} - {self.nhif_number} - {self.payment_date}"
    

class DoctorAppointment(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    symptoms = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user_name} on {self.appointment_date}"



class TBPatient(models.Model):
    IDENTIFICATION_CHOICES = [
        ('National ID', 'National ID'),
        ('Passport', 'Passport'),
        ('Alien ID', 'Alien ID'),
    ]
     
    TB_STAGES = [
        ('Latent TB', 'Latent TB'),
        ('Active TB', 'Active TB'),
        ('MDR-TB', 'MDR-TB'),  # Multi-drug resistant TB
        ('XDR-TB', 'XDR-TB'),  # Extensively drug-resistant TB
    ]

    VACCINE_CHOICES = [
        ('BCG', 'BCG'),  # Bacille Calmette-Guerin vaccine
        ('Vaccine X', 'Vaccine X'),
        ('Vaccine Y', 'Vaccine Y'),
    ]

    # Patient information
    user_name = models.CharField(max_length=100, unique=True)
    identification_no = models.CharField(max_length=20, unique=True)
    identification_type = models.CharField(max_length=20, choices=IDENTIFICATION_CHOICES, default='National ID')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()  # Date of birth
    diagnosis_date = models.DateField(default=timezone.now)  # Date the patient was diagnosed with TB
    county = models.CharField(max_length=100,  null=True, blank=True) 
    # TB-specific data

    tb_stage = models.CharField(max_length=50, choices=TB_STAGES, default='Latent TB')
    vaccine_received = models.CharField(max_length=50, choices=VACCINE_CHOICES)
    vaccine_effectiveness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Effectiveness of vaccine in percentage
    
    # Week-by-week progress (percentage of recovery)
    week_1 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    week_2 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    week_3 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    week_4 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    week_5 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    week_6 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    week_7 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    week_8 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    week_9 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    week_10 = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    # Treatment details
    treatment_start_date = models.DateField(null=True, blank=True)  # Treatment start date
    treatment_end_date = models.DateField(null=True, blank=True)  # Treatment end date
    treatment_notes = models.TextField()  # Notes on the treatment process
    
    # Performance and follow-up
    performance_status = models.TextField()  # Text field to track how the patient has been responding to treatment
    follow_up_date = models.DateField(null=True, blank=True)  # Date for next follow-up

    def __str__(self):
        return f"{self.user_name} - {self.identification_no}"

    class Meta:
        verbose_name = 'TB Patient'
        verbose_name_plural = 'TB Patients'


class Region(models.Model):
    name = models.CharField(max_length=255)  # Region name
    
    
    def __str__(self):
        return self.name



class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='hospitals')  # Link to Region
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return self.name

class Medication(models.Model):
    name = models.CharField(max_length=255)  # Medication name
    dosage = models.CharField(max_length=100)  # Dosage information
    side_effects = models.TextField()  # Side effects of the medication
    availability = models.CharField(max_length=255)  # Where to find the medication (e.g., pharmacy)
    
    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    preventive_measures = models.TextField()
    treatment_info = models.TextField()
    image = models.ImageField(upload_to='disease_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='disease_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='disease_images/', null=True, blank=True)
    affected_regions = models.ManyToManyField(Region, related_name='diseases')  # Areas affected
    medications = models.ManyToManyField(Medication, related_name='diseases')  # Related medications
    
    
    def __str__(self):
        return self.name