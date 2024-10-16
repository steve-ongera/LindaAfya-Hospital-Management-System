# Generated by Django 4.2.3 on 2024-10-08 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_nhifpayment'),
    ]

    operations = [
        migrations.CreateModel(
            name='KenyaHospitalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identification_no', models.CharField(max_length=20, unique=True)),
                ('identification_type', models.CharField(choices=[('National ID', 'National ID'), ('Passport', 'Passport'), ('Alien ID', 'Alien ID')], default='National ID', max_length=20)),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nhif_no', models.CharField(max_length=50, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('is_doctor', models.BooleanField(default=False)),
                ('is_patient', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Hospital User',
                'verbose_name_plural': 'Hospital Users',
            },
        ),
    ]
