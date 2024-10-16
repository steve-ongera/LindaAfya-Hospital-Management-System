# Generated by Django 4.2.3 on 2024-10-07 19:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_patient_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='NHIFPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nhif_number', models.CharField(max_length=20)),
                ('payment_date', models.DateField(default=django.utils.timezone.now)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(choices=[('MPESA', 'Mpesa'), ('Bank', 'Bank Transfer'), ('Cash', 'Cash')], max_length=50)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nhif_payments', to='hospital.patient')),
            ],
        ),
    ]
