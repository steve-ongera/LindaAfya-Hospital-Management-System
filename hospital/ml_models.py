import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import joblib


def train_and_save_models(data_path):
    # Load data
    df = pd.read_csv(data_path)
    
    # Data preprocessing (similar to the previous script)
    df['age'] = (pd.to_datetime(df['diagnosis_date']) - pd.to_datetime(df['dob'])).astype('<m8[Y]')
    df['treatment_duration'] = (pd.to_datetime(df['treatment_end_date']) - pd.to_datetime(df['treatment_start_date'])).dt.days
    df = pd.get_dummies(df, columns=['identification_type', 'tb_stage', 'vaccine_received'])
    
    # Prepare features and target variables
    X = df[['age', 'vaccine_effectiveness', 'treatment_duration', 'identification_type_National ID', 
            'identification_type_Passport', 'identification_type_Alien ID', 'tb_stage_Latent TB', 
            'tb_stage_Active TB', 'tb_stage_MDR-TB', 'tb_stage_XDR-TB', 'vaccine_received_BCG', 
            'vaccine_received_Vaccine X', 'vaccine_received_Vaccine Y']]
    y_county = df['county']
    y_spread = df[['week_1', 'week_2', 'week_3', 'week_4', 'week_5', 'week_6', 'week_7', 'week_8', 'week_9', 'week_10']].mean(axis=1)
    
    # Split the data
    X_train, X_test, y_county_train, y_county_test, y_spread_train, y_spread_test = train_test_split(
        X, y_county, y_spread, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Train models
    county_model = RandomForestClassifier(n_estimators=100, random_state=42)
    county_model.fit(X_train_scaled, y_county_train)
    
    spread_model = RandomForestRegressor(n_estimators=100, random_state=42)
    spread_model.fit(X_train_scaled, y_spread_train)
    
    # Save models and scaler
    joblib.dump(county_model, 'county_model.joblib')
    joblib.dump(spread_model, 'spread_model.joblib')
    joblib.dump(scaler, 'scaler.joblib')
    
    print("Models trained and saved successfully.")

def load_models():
    county_model = joblib.load('county_model.joblib')
    spread_model = joblib.load('spread_model.joblib')
    scaler = joblib.load('scaler.joblib')
    return county_model, spread_model, scaler

def predict_tb_spread(patient_data):
    county_model, spread_model, scaler = load_models()
    
    patient_df = pd.DataFrame([patient_data])
    patient_encoded = pd.get_dummies(patient_df, columns=['identification_type', 'tb_stage', 'vaccine_received'])
    
    # Ensure all columns are present
    expected_columns = ['age', 'vaccine_effectiveness', 'treatment_duration', 'identification_type_National ID', 
                        'identification_type_Passport', 'identification_type_Alien ID', 'tb_stage_Latent TB', 
                        'tb_stage_Active TB', 'tb_stage_MDR-TB', 'tb_stage_XDR-TB', 'vaccine_received_BCG', 
                        'vaccine_received_Vaccine X', 'vaccine_received_Vaccine Y']
    
    for col in expected_columns:
        if col not in patient_encoded.columns:
            patient_encoded[col] = 0
    
    patient_features = patient_encoded[expected_columns]
    patient_scaled = scaler.transform(patient_features)
    
    county_prediction = county_model.predict(patient_scaled)[0]
    spread_prediction = spread_model.predict(patient_scaled)[0]
    
    return county_prediction, spread_prediction

