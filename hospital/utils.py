# tb_prediction/utils.py

import pandas as pd
from .models import TBPatient

def fetch_patient_data():
    patients = TBPatient.objects.all()
    data = []
    for patient in patients:
        data.append({
            'age': (pd.to_datetime('today') - patient.dob).days // 365,
            'county': patient.county,
            'tb_stage': patient.tb_stage,
            'vaccine_received': patient.vaccine_received,
            'vaccine_effectiveness': patient.vaccine_effectiveness,
            # Include other features as needed
        })
    return pd.DataFrame(data)


# tb_prediction/utils.py

import joblib

def load_model():
    return joblib.load('tb_prediction/model.pkl')
