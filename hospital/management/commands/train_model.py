# tb_prediction/management/commands/train_model.py

from django.core.management.base import BaseCommand
import joblib
import pandas as pd
from hospital.models import TBPatient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # or any model you prefer
from datetime import datetime

class Command(BaseCommand):
    help = 'Train the TB prediction model and save it as model.pkl'

    def handle(self, *args, **kwargs):
        # Load your TBPatient data from the database
        data = TBPatient.objects.all().values()  # Fetch all records
        df = pd.DataFrame(data)

        # Check if 'dob' column is present
        if 'dob' not in df.columns:
            self.stdout.write(self.style.ERROR('dob column is missing in the dataset.'))
            return

        # Ensure 'dob' is in datetime format
        df['dob'] = pd.to_datetime(df['dob'], errors='coerce')  # Convert dob to datetime

        # Calculate age in a simple way
        today = datetime.now()
        df['age'] = today.year - df['dob'].dt.year
        df['age'] = df['age'] - ((today.month, today.day) < (df['dob'].dt.month, df['dob'].dt.day)).astype(int)

        # Ensure that necessary columns exist
        required_columns = ['age', 'vaccine_received', 'tb_stage']
        for col in required_columns:
            if col not in df.columns:
                self.stdout.write(self.style.ERROR(f'{col} column is missing in the dataset.'))
                return

        # Prepare features and target variable
        X = df[required_columns]  # Use relevant features
        y = df['tb_stage']  # Target variable (ensure this is correct)

        # Convert categorical variables to dummy variables if necessary
        X = pd.get_dummies(X)

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # Train the model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Save the model
        model_path = 'hospital/model.pkl'
        joblib.dump(model, model_path)

        self.stdout.write(self.style.SUCCESS('Model trained and saved successfully!'))
