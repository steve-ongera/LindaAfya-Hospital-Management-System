# Generated by Django 4.2.3 on 2024-10-09 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0008_tbpatient'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbpatient',
            name='county',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
