from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login ,  logout
from .forms import CustomUserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
import calendar
from decimal import Decimal
from collections import Counter
from collections import defaultdict
from .utils import load_model
import pandas as pd

def home(request):
    return render(request, 'home.html')

# List all Patient entries
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

# Create a new Patient entry

def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            form.save()
            return redirect('patient_list')  # Redirect to the patient list or another view
    else:
        form = PatientForm()
    return render(request, 'patient_form.html', {'form': form})

# Update an existing Patient entry
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')  # Redirect to the list view
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient_form.html', {'form': form})

# Delete a Patient entry
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')  # Redirect to the list view
    return render(request, 'patient_confirm_delete.html', {'patient': patient})

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    context = {
        'patient': patient,
    }
    return render(request, 'patient_detail.html', context)

# List all NonStaff entries
def nonstaff_list(request):
    nonstaffs = NonStaff.objects.all()
    return render(request, 'nonstaff_list.html', {'nonstaffs': nonstaffs})

# Create a new NonStaff entry
def nonstaff_create(request):
    if request.method == 'POST':
        form = NonStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nonstaff_list')  # Redirect to the list view
    else:
        form = NonStaffForm()
    return render(request, 'nonstaff_form.html', {'form': form})

# Update an existing NonStaff entry
def nonstaff_update(request, pk):
    nonstaff = get_object_or_404(NonStaff, pk=pk)
    if request.method == 'POST':
        form = NonStaffForm(request.POST, instance=nonstaff)
        if form.is_valid():
            form.save()
            return redirect('nonstaff_list')  # Redirect to the list view
    else:
        form = NonStaffForm(instance=nonstaff)
    return render(request, 'nonstaff_form.html', {'form': form})

# Delete a NonStaff entry
def nonstaff_delete(request, pk):
    nonstaff = get_object_or_404(NonStaff, pk=pk)
    if request.method == 'POST':
        nonstaff.delete()
        return redirect('nonstaff_list')  # Redirect to the list view
    return render(request, 'nonstaff_confirm_delete.html', {'nonstaff': nonstaff})



@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})


@login_required
def manage_nonstaff(request):
    nonstaff = NonStaff.objects.all()
    if request.method == 'POST':
        form = NonStaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_nonstaff')
    else:
        form = NonStaffForm()
    return render(request, 'manage_nonstaff.html', {'form': form, 'nonstaff': nonstaff})

@login_required
def update_exit_time(request, nonstaff_id):
    nonstaff = NonStaff.objects.get(id=nonstaff_id)
    if request.method == 'POST':
        nonstaff.exit_time = request.POST.get('exit_time')
        nonstaff.save()
        return redirect('manage_nonstaff')
    return render(request, 'update_exit_time.html', {'nonstaff': nonstaff})



# List all Doctor entries
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})

# Create a new Doctor entry
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')  # Redirect to the list view
    else:
        form = DoctorForm()
    return render(request, 'doctor_form.html', {'form': form})

# Update an existing Doctor entry
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')  # Redirect to the list view
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctor_form.html', {'form': form})

# Delete a Doctor entry
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')  # Redirect to the list view
    return render(request, 'doctor_confirm_delete.html', {'doctor': doctor})

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    context = {
        'doctor': doctor,
    }
    return render(request, 'doctor_detail.html', context)


# List all Staff entries
def staff_list(request):
    staff_members = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff_members': staff_members})

# Create a new Staff entry
def staff_create(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')  # Redirect to the list view
    else:
        form = StaffForm()
    return render(request, 'staff_form.html', {'form': form})

# Update an existing Staff entry
def staff_update(request, pk):
    staff_member = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff_member)
        if form.is_valid():
            form.save()
            return redirect('staff_list')  # Redirect to the list view
    else:
        form = StaffForm(instance=staff_member)
    return render(request, 'staff_form.html', {'form': form})

# Delete a Staff entry
def staff_delete(request, pk):
    staff_member = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff_member.delete()
        return redirect('staff_list')  # Redirect to the list view
    return render(request, 'staff_confirm_delete.html', {'staff_member': staff_member})


def nhif_payment_list(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    nhif_payments = NHIFPayment.objects.filter(patient=patient)
    return render(request, 'nhif_payment_list.html', {'patient': patient, 'nhif_payments': nhif_payments})


def nhif_payment_list_all(request):
    nhif_payments = NHIFPayment.objects.all()  # Fetch all NHIF payments
    return render(request, 'nhif_payment_list_all.html', {'nhif_payments': nhif_payments})


# View to add a new NHIF payment
@login_required
def nhif_payment_add(request):
    if request.method == 'POST':
        form = NHIFPaymentForm(request.POST)
        if form.is_valid():
            nhif_payment = form.save(commit=False)

            # Check if the patient exists in the Patient model
            patient_id = request.POST.get('patient')
            if not patient_id:
                return render(request, 'error.html', {'message': 'Patient ID is missing.'})

            try:
                patient = get_object_or_404(Patient, pk=patient_id)
            except Patient.DoesNotExist:
                return render(request, 'error.html', {'message': 'Patient not found.'})

            # Assign the patient to the NHIF payment
            nhif_payment.patient = patient
            nhif_payment.save()

            return redirect('nhif_payment_list_all')
    else:
        form = NHIFPaymentForm()

    # Filter only patients when rendering the form
    patients = Patient.objects.all()
    return render(request, 'nhif_payment_add.html', {'form': form, 'patients': patients})


# View to update an existing NHIF payment
def nhif_payment_update(request, pk):
    nhif_payment = get_object_or_404(NHIFPayment, pk=pk)
    if request.method == 'POST':
        form = NHIFPaymentForm(request.POST, instance=nhif_payment)
        if form.is_valid():
            form.save()
            return redirect('nhif_payment_list_all')
    else:
        form = NHIFPaymentForm(instance=nhif_payment)
    return render(request, 'nhif_payment_update.html', {'form': form})

# View to delete an existing NHIF payment
def nhif_payment_delete(request, pk):
    nhif_payment = get_object_or_404(NHIFPayment, pk=pk)
    if request.method == 'POST':
        nhif_payment.delete()
        return redirect('nhif_payment_list_all')
    return render(request, 'nhif_payment_confirm_delete.html', {'nhif_payment': nhif_payment})


@login_required
def patient_dashboard(request):
    # Get the logged-in user’s patient profile
    patient = get_object_or_404(Patient, user_name=request.user.username)

    # Get NHIF payment data for the patient
    nhif_payments = NHIFPayment.objects.filter(patient=patient)

    # Initialize data for the graph
    payments_by_month = [0] * 12  # For January to December

    # Loop over payments and sum amounts per month
    for payment in nhif_payments:
        month = payment.payment_date.month
        payments_by_month[month - 1] += float(payment.amount_paid)  # Convert Decimal to float

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    context = {
        'patient': patient,
        'nhif_payments': nhif_payments,
        'payments_by_month': payments_by_month,
        'months': months,
    }

    return render(request, 'patient_dashboard.html', context)





def register(request):
    if request.method == 'POST':
        # Collect form data
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        identification_no = request.POST.get('identification_no')
        password = request.POST.get('password')

        # Check if the username, names, and identification_no exist in KenyaHospitalData
        try:
            hospital_user = KenyaHospitalData.objects.get(
                user_name=username,
                first_name=first_name,
                last_name=last_name,
                identification_no=identification_no
            )
        except KenyaHospitalData.DoesNotExist:
            messages.error(request, 'No matching records found in Kenya Hospital Database. Please verify your details.')
            return render(request, 'register.html')

        # Ensure the user does not already exist
        if User.objects.filter(username=username).exists():
            messages.error(request, 'A user with this username already exists.')
            return render(request, 'register.html')

        # Create the user and set the password
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=hospital_user.email,  # Use email from the KenyaHospitalData record
            password=make_password(password)  # Hash the password
        )

        # Automatically log the user in after registration
        login(request, user)

        # Create a profile for the user based on their role in KenyaHospitalData
        if hospital_user.is_patient:
            # Create a Patient profile
            Patient.objects.create(
                user_name=user.username,
                dob='1990-01-01',  # Placeholder date, can be replaced with a real DOB if available
                gender='Not Specified',  # Placeholder gender, can be replaced with actual value
                phone=hospital_user.phone,
                identification_no=hospital_user.identification_no,
                address=hospital_user.address,
                contact_info=hospital_user.phone,
                medical_history='No medical history available'  # Placeholder for medical history
            )
            messages.success(request, 'Patient profile created successfully!')

        elif hospital_user.is_doctor:
            # Create a Doctor profile
            Doctor.objects.create(
                user_name=user.username,
                specialization='General Medicine',  # Placeholder specialization, can be replaced
                schedule='Not available'  # Placeholder for schedule
            )
            messages.success(request, 'Doctor profile created successfully!')

        # Successful registration message
        messages.success(request, 'Your account has been created successfully!')
        return redirect('home')  # Redirect to a home page or dashboard after successful registration

    return render(request, 'register.html')


def simple_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Check if the user is a patient or a doctor
            try:
                profile = KenyaHospitalData.objects.get(user_name=username)

                if profile.is_patient:
                    return redirect('patient_dashboard')  # Redirect to patient dashboard
                elif profile.is_doctor:
                    return redirect('doctor_dashboard')   # Redirect to doctor dashboard
                else:
                    messages.error(request, 'Error 404')
                    return redirect('home')  # Redirect to error page if user is neither
            except KenyaHospitalData.DoesNotExist:
                messages.error(request, 'Error 404')
                return redirect('home')  # Redirect to error page if no profile found
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def simple_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


@login_required
def doctor_dashboard(request):
    # Get the logged-in doctor's profile
    try:
        doctor = Doctor.objects.get(user_name=request.user.username)
    except Doctor.DoesNotExist:
        return render(request, 'error.html', {'message': 'Doctor profile not found.'})

    # Fetch assigned patients
    patients = doctor.patients.all()

    # Context to pass to the template
    context = {
        'doctor': doctor,
        'patients': patients,
    }
    
    return render(request, 'doctor_dashboard.html', context)



@login_required
def book_doctor(request):
    # Get the logged-in user's patient profile
    patient = get_object_or_404(Patient, user_name=request.user.username)

    if request.method == 'POST':
        form = DoctorAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient  # Assign the logged-in patient
            appointment.save()
            return redirect('appointment_success')
    else:
        form = DoctorAppointmentForm()

    context = {
        'form': form,
    }
    return render(request, 'book_doctor.html', context)



def appointment_success(request):
    return render(request, 'appointment_success.html')

@login_required
def view_patient_appointments(request):
    # Get the logged-in patient's profile
    patient = get_object_or_404(Patient, user_name=request.user.username)
    
    # Fetch only appointments related to the logged-in patient
    appointments = DoctorAppointment.objects.filter(patient=patient)
    
    context = {
        'appointments': appointments,
    }
    
    return render(request, 'view_patient_appointments.html', context)

@login_required
def update_appointment(request, appointment_id):
    # Get the appointment object
    appointment = get_object_or_404(DoctorAppointment, id=appointment_id)

    # Check if the appointment belongs to the logged-in patient
    if appointment.patient.user_name != request.user.username:
        return redirect('view_patient_appointments')  # Redirect if not authorized

    if request.method == 'POST':
        form = DoctorAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('view_patient_appointments')  # Redirect after update
    else:
        form = DoctorAppointmentForm(instance=appointment)

    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'update_appointment.html', context)


@login_required
def delete_appointment(request, appointment_id):
    # Get the appointment object
    appointment = get_object_or_404(DoctorAppointment, id=appointment_id)

    # Check if the appointment belongs to the logged-in patient
    if appointment.patient.user_name != request.user.username:
        return redirect('view_patient_appointments')  # Redirect if not authorized

    if request.method == 'POST':
        appointment.delete()
        return redirect('view_patient_appointments')  # Redirect after deletion

    context = {
        'appointment': appointment,
    }
    return render(request, 'delete_appointment.html', context)



@login_required
def doctor_appointments(request):
    # Get the logged-in doctor's appointments
    appointments = DoctorAppointment.objects.filter(doctor__user_name=request.user.username)

    context = {
        'appointments': appointments,
    }
    return render(request, 'doctor_appointments.html', context)




def tb_patient_add(request):
    if request.method == 'POST':
        form = TBPatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tb_patient_list')  # Redirect to the TB patients list
    else:
        form = TBPatientForm()
    return render(request, 'tb_patient_add.html', {'form': form})

def tb_patient_list(request):
    tb_patients = TBPatient.objects.all()  # Retrieve all TB patients from the database
    return render(request, 'tb_patient_list.html', {'tb_patients': tb_patients})


def tb_patient_detail(request, pk):
    tb_patient = get_object_or_404(TBPatient, pk=pk)  # Get the specific TB patient using primary key

    # Prepare the data for the graph
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 
             'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10']
    
    # Convert Decimal values to float
    performance_data = [
        float(tb_patient.week_1), float(tb_patient.week_2), float(tb_patient.week_3),
        float(tb_patient.week_4), float(tb_patient.week_5), float(tb_patient.week_6),
        float(tb_patient.week_7), float(tb_patient.week_8), float(tb_patient.week_9),
        float(tb_patient.week_10)
    ]

    context = {
        'tb_patient': tb_patient,
        'weeks': weeks,
        'performance_data': performance_data,
    }
    return render(request, 'tb_patient_detail.html', context)


def tb_patient_update(request, pk):
    tb_patient = get_object_or_404(TBPatient, pk=pk)  # Fetch the TB patient
    if request.method == 'POST':
        form = TBPatientForm(request.POST, instance=tb_patient)
        if form.is_valid():
            form.save()
            return redirect('tb_patient_detail', pk=tb_patient.pk)
    else:
        form = TBPatientForm(instance=tb_patient)
    return render(request, 'tb_patient_update.html', {'form': form, 'tb_patient': tb_patient})


def tb_patient_delete(request, pk):
    tb_patient = get_object_or_404(TBPatient, pk=pk)
    if request.method == 'POST':
        tb_patient.delete()
        return redirect('tb_patient_list')
    return render(request, 'tb_patient_delete_confirm.html', {'tb_patient': tb_patient})


def vaccine_performance(request):
    patients = TBPatient.objects.all()
    vaccine_data = []

    for patient in patients:
        weekly_progress = [
            patient.week_1,
            patient.week_2,
            patient.week_3,
            patient.week_4,
            patient.week_5,
            patient.week_6,
            patient.week_7,
            patient.week_8,
            patient.week_9,
            patient.week_10,
        ]
        average_progress = sum(weekly_progress) / len(weekly_progress)  # Calculate average progress
        vaccine_data.append({
            'user_name': patient.user_name,
            'vaccine_received': patient.vaccine_received.lower(),  # Convert to lowercase
            'average_progress': average_progress,
            'vaccine_effectiveness': patient.vaccine_effectiveness,
            'weekly_progress': weekly_progress,
        })

    # Prepare data for the pie chart (vaccine distribution)
    vaccine_counts = Counter(patient.vaccine_received for patient in patients)
    vaccines = list(vaccine_counts.keys())
    vaccine_values = list(vaccine_counts.values())
    
    # Define colors for each vaccine
    vaccine_colors = {
        'BCG': 'rgba(75, 192, 192, 0.6)',  # teal
        'Vaccine X': 'rgba(255, 99, 132, 0.6)',  # red
        'Vaccine Y': 'rgba(255, 206, 86, 0.6)',  # yellow
        'Vaccine Z': 'green',
    }

    # Prepare data for bar chart and pie chart
    vaccine_counts = defaultdict(int)
    performance_data = defaultdict(list)

    for patient in patients:
        vaccine_counts[patient.vaccine_received] += 1
        performance_data[patient.vaccine_received].append(patient.vaccine_effectiveness)
    
    # Prepare data for bar chart
    bar_labels = list(vaccine_counts.keys())
    bar_data = list(vaccine_counts.values())
    bar_colors = [vaccine_colors[vaccine] for vaccine in bar_labels]  # Get colors for bar chart
    
    # Prepare data for pie chart
    pie_data = list(vaccine_counts.values())
    pie_colors = [vaccine_colors[vaccine] for vaccine in bar_labels]  # Use same colors for pie chart

    context = {
        'bar_labels': bar_labels,
        'bar_data': bar_data,
        'bar_colors': bar_colors,
        'pie_data': pie_data,
        'pie_labels': bar_labels,
        'pie_colors': pie_colors,
        'patients': patients,  # Pass the patient data for rendering the HTML
        'vaccine_data': vaccine_data,
        'vaccines': vaccines,
        'vaccine_values': vaccine_values,
    }
    return render(request, 'vaccine_performance.html', context)



from collections import defaultdict

def vaccine_analysis(request):
    patients = TBPatient.objects.all()
    
    performance_data = defaultdict(lambda: defaultdict(list))
    
    for patient in patients:
        performance_data[patient.vaccine_received]['weeks'].append([
            patient.week_1,
            patient.week_2,
            patient.week_3,
            patient.week_4,
            patient.week_5,
            patient.week_6,
            patient.week_7,
            patient.week_8,
            patient.week_9,
            patient.week_10,
        ])
    
    vaccine_effectiveness = {}
    vaccine_colors = {
        'BCG': 'rgba(75, 192, 192, 0.6)',  # teal
        'Vaccine X': 'rgba(255, 99, 132, 0.6)',  # red
        'Vaccine Y': 'rgba(255, 206, 86, 0.6)',  # yellow
        'Vaccine Z': 'rgba(54, 162, 235, 0.6)',  # blue
    }

    for vaccine, data in performance_data.items():
        if data['weeks']:
            weeks_data = list(zip(*data['weeks']))  # Transpose to get weeks data
            average_effectiveness = [sum(week) / len(week) for week in weeks_data]  # Average for each week
            vaccine_effectiveness[vaccine] = average_effectiveness

    average_vaccine_scores = {vaccine: sum(scores)/len(scores) for vaccine, scores in vaccine_effectiveness.items()}
    sorted_vaccines = sorted(average_vaccine_scores.items(), key=lambda x: x[1])

    context = {
        'vaccine_effectiveness': vaccine_effectiveness,
        'sorted_vaccines': sorted_vaccines,
        'vaccine_colors': vaccine_colors,
    }
    
    return render(request, 'vaccine_analysis.html', context)


def county_victims_analysis(request):
    # Get all patients and group them by county
    patients = TBPatient.objects.all()
    
    # Count patients by county
    county_counts = Counter(patient.county for patient in patients if patient.county)
    
    # Separate the county names and the respective counts
    counties = list(county_counts.keys())
    victim_counts = list(county_counts.values())
    
    # Pass the county names and counts to the template
    context = {
        'counties': counties,
        'victim_counts': victim_counts,
    }
    
    return render(request, 'county_victims_analysis.html', context)


def tb_patients_map(request):
    # Group TB patients by county
    county_data = TBPatient.objects.values('county').annotate(victims=models.Count('id'))
    
    counties_data = []
    for data in county_data:
        counties_data.append({
            'name': data['county'],
            'victims': data['victims'],
            'location': get_county_location(data['county']),  # Function to return latitude and longitude
        })

    return render(request, 'map.html', {'counties_data': counties_data})

def get_county_location(county_name):
    # Return coordinates for each county (Add more counties and their coordinates)
    locations = {
        'Muranga': {'lat': -0.7831, 'lng': 37.0351},
        'Kisumu': {'lat': -0.0917, 'lng': 34.7680},
        'Mombasa': {'lat': -4.0435, 'lng': 39.6682},
        'Nairobi': {'lat': -1.286389, 'lng': 36.817223},
        'Nakuru': {'lat': -0.3031, 'lng': 36.0800},
        'Uasin Gishu': {'lat': 0.5143, 'lng': 35.2698},
        'Homa Bay': {'lat': -0.5273, 'lng': 34.4571},
        'Kilifi': {'lat': -3.5107, 'lng': 39.9093},
        'Kiambu': {'lat': -1.1741, 'lng': 36.8344},
        'Marsabit': {'lat': 2.3333, 'lng': 37.9833},
        'Baringo': {'lat': 0.4656, 'lng': 35.9529},
        'Bomet': {'lat': -0.7820, 'lng': 35.3391},
        'Bungoma': {'lat': 0.5636, 'lng': 34.5608},
        'Busia': {'lat': 0.4347, 'lng': 34.2422},
        'Elgeyo-Marakwet': {'lat': 0.4905, 'lng': 35.4596},
        'Embu': {'lat': -0.5373, 'lng': 37.4591},
        'Garissa': {'lat': -0.4532, 'lng': 39.6460},
        'Isiolo': {'lat': 0.3546, 'lng': 37.5820},
        'Kajiado': {'lat': -1.8537, 'lng': 36.7768},
        'Kakamega': {'lat': 0.2827, 'lng': 34.7519},
        'Kericho': {'lat': -0.3689, 'lng': 35.2834},
        'Kirinyaga': {'lat': -0.6880, 'lng': 37.2831},
        'Kitui': {'lat': -1.3667, 'lng': 38.0100},
        'Kwale': {'lat': -4.1833, 'lng': 39.4500},
        'Laikipia': {'lat': 0.2164, 'lng': 36.8815},
        'Lamu': {'lat': -2.2713, 'lng': 40.9020},
        'Machakos': {'lat': -1.5177, 'lng': 37.2634},
        'Makueni': {'lat': -1.8030, 'lng': 37.6310},
        'Mandera': {'lat': 3.9366, 'lng': 41.8670},
        'Meru': {'lat': 0.0474, 'lng': 37.6496},
        'Migori': {'lat': -1.0631, 'lng': 34.4736},
        'Narok': {'lat': -1.0782, 'lng': 35.8646},
        'Nyamira': {'lat': -0.5634, 'lng': 34.9357},
        'Nyandarua': {'lat': -0.1549, 'lng': 36.3870},
        'Nyeri': {'lat': -0.4164, 'lng': 36.9510},
        'Samburu': {'lat': 1.1827, 'lng': 36.7209},
        'Siaya': {'lat': -0.0606, 'lng': 34.2422},
        'Taita-Taveta': {'lat': -3.3167, 'lng': 38.3667},
        'Tana River': {'lat': -1.3979, 'lng': 40.0100},
        'Tharaka-Nithi': {'lat': -0.2970, 'lng': 37.8028},
        'Trans Nzoia': {'lat': 1.0161, 'lng': 35.0036},
        'Turkana': {'lat': 3.5262, 'lng': 35.8534},
        'Vihiga': {'lat': 0.0847, 'lng': 34.7242},
        'Wajir': {'lat': 1.7500, 'lng': 40.0667},
        'West Pokot': {'lat': 1.2381, 'lng': 35.1328},
        'Kisii': {'lat': -0.6773, 'lng': 34.7799},
        'Nyamira': {'lat': -0.5703, 'lng': 34.9347},



        # Add more counties...
    }
    return locations.get(county_name, {'lat': -1.286389, 'lng': 36.817223})  # Default to Nairobi if not found


@login_required
def patient_profile(request):
    # Get the logged-in user's username
    user_name = request.user.username
    
    # Try to fetch the TBPatient data that matches the logged-in user's username
    try:
        patient_data = TBPatient.objects.get(user_name=user_name)
    except TBPatient.DoesNotExist:
        # Render the error template if no TBPatient matches
        return render(request, '404.html', {'message': 'No TBPatient matches the given query.'})
    
    context = {
        'patient': patient_data
    }
    
    return render(request, 'patient_profile.html', context)


def predict_tb_risk(request):
    if request.method == 'POST':
        # Get data from the form
        age = request.POST['age']
        county = request.POST['county']
        tb_stage = request.POST['tb_stage']
        vaccine_received = request.POST['vaccine_received']
        vaccine_effectiveness = request.POST['vaccine_effectiveness']

        # Create DataFrame for prediction
        input_data = pd.DataFrame({
            'age': [age],
            'county': [county],
            'tb_stage': [tb_stage],
            'vaccine_received': [vaccine_received],
            'vaccine_effectiveness': [vaccine_effectiveness],
        })

        # Load the model and make a prediction
        model = load_model()
        prediction = model.predict(input_data)

        context = {'prediction': prediction}
        return render(request, 'tb_prediction/result.html', context)

    return render(request, 'tb_prediction/form.html')

#new model
from .ml_models import predict_tb_spread
from datetime import datetime

def predict_tb(request, patient_id):
    patient = TBPatient.objects.get(id=patient_id)
    
    # Prepare patient data for prediction
    patient_data = {
        'age': (datetime.now().date() - patient.dob).days // 365,
        'vaccine_effectiveness': patient.vaccine_effectiveness,
        'treatment_duration': (patient.treatment_end_date - patient.treatment_start_date).days if patient.treatment_end_date else 0,
        'identification_type': patient.identification_type,
        'tb_stage': patient.tb_stage,
        'vaccine_received': patient.vaccine_received
    }
    
    predicted_county, predicted_spread = predict_tb_spread(patient_data)
    
    context = {
        'patient': patient,
        'predicted_county': predicted_county,
        'predicted_spread': predicted_spread
    }
    
    return render(request, 'predict_tb.html', context)