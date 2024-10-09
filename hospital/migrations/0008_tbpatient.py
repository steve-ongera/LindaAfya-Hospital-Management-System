# Generated by Django 4.2.3 on 2024-10-09 09:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0007_doctorappointment'),
    ]

    operations = [
        migrations.CreateModel(
            name='TBPatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('identification_no', models.CharField(max_length=20, unique=True)),
                ('identification_type', models.CharField(choices=[('National ID', 'National ID'), ('Passport', 'Passport'), ('Alien ID', 'Alien ID')], default='National ID', max_length=20)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('diagnosis_date', models.DateField(default=django.utils.timezone.now)),
                ('tb_stage', models.CharField(choices=[('Latent TB', 'Latent TB'), ('Active TB', 'Active TB'), ('MDR-TB', 'MDR-TB'), ('XDR-TB', 'XDR-TB')], default='Latent TB', max_length=50)),
                ('vaccine_received', models.CharField(choices=[('BCG', 'BCG'), ('Vaccine X', 'Vaccine X'), ('Vaccine Y', 'Vaccine Y')], max_length=50)),
                ('vaccine_effectiveness', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('week_1', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('week_2', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('week_3', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('week_4', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('week_5', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('week_6', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('week_7', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('week_8', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('week_9', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('week_10', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('treatment_start_date', models.DateField(blank=True, null=True)),
                ('treatment_end_date', models.DateField(blank=True, null=True)),
                ('treatment_notes', models.TextField()),
                ('performance_status', models.TextField()),
                ('follow_up_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'TB Patient',
                'verbose_name_plural': 'TB Patients',
            },
        ),
    ]
