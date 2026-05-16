import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import r2_score
import joblib
import os

os.makedirs('models', exist_ok=True)

def generate_dataset(num_rows=10000):
    print("Generating MediGuide AI dataset...")
    np.random.seed(42)
    
    diseases = ['Heart Bypass', 'Knee Replacement', 'Spinal Fusion', 'Cataract Surgery', 'Dental Implants', 'Cosmetic Surgery', 'Oncology', 'Neurology', 'Orthopedics']
    countries = ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'UAE', 'India', 'Thailand', 'Turkey', 'Singapore']
    hospital_types = ['Public', 'Private', 'Premium International', 'Luxury Medical Resort']
    doctor_experiences = ['1-5 Years', '5-10 Years', '10-20 Years', '20+ Years']
    travel_classes = ['Economy', 'Business', 'First Class']
    room_types = ['General Ward', 'Semi-Private', 'Private', 'VIP Suite']
    insurances = ['No Insurance', 'Partial', 'Full']
    cities = ['New York', 'London', 'Dubai', 'Singapore', 'Bangkok', 'Istanbul', 'Mumbai']
    
    data = []
    
    for _ in range(num_rows):
        disease = np.random.choice(diseases)
        country = np.random.choice(countries)
        hospital_type = np.random.choice(hospital_types)
        doctor_exp = np.random.choice(doctor_experiences)
        travel_class = np.random.choice(travel_classes)
        room_type = np.random.choice(room_types)
        insurance = np.random.choice(insurances)
        city = np.random.choice(cities)
        
        stay_days = np.random.randint(1, 45)
        
        # Base logic for costs
        treatment_cost = np.random.uniform(3000, 25000)
        if disease in ['Heart Bypass', 'Oncology', 'Neurology']: treatment_cost *= 2.5
        elif disease in ['Dental Implants', 'Cataract Surgery']: treatment_cost *= 0.4
        
        if hospital_type == 'Premium International': treatment_cost *= 1.5
        elif hospital_type == 'Luxury Medical Resort': treatment_cost *= 2.5
        
        if doctor_exp == '20+ Years': treatment_cost *= 1.3
        
        travel_cost = np.random.uniform(500, 2000)
        if travel_class == 'Business': travel_cost *= 3
        elif travel_class == 'First Class': travel_cost *= 6
        
        daily_room_rate = 100
        if room_type == 'Semi-Private': daily_room_rate = 200
        elif room_type == 'Private': daily_room_rate = 500
        elif room_type == 'VIP Suite': daily_room_rate = 1500
        
        stay_cost = daily_room_rate * stay_days
        
        medicine_cost = treatment_cost * np.random.uniform(0.05, 0.20)
        
        # Add noise
        treatment_cost += np.random.normal(0, treatment_cost * 0.05)
        travel_cost += np.random.normal(0, travel_cost * 0.05)
        stay_cost += np.random.normal(0, stay_cost * 0.05)
        medicine_cost += np.random.normal(0, medicine_cost * 0.05)
        
        total_cost = treatment_cost + travel_cost + stay_cost + medicine_cost
        
        # Insurance deduction
        if insurance == 'Partial': total_cost *= 0.6
        elif insurance == 'Full': total_cost *= 0.1
        
        data.append({
            'Disease': disease,
            'Country': country,
            'Hospital_Type': hospital_type,
            'Stay_Days': stay_days,
            'Travel_Class': travel_class,
            'Room_Type': room_type,
            'Doctor_Experience': doctor_exp,
            'Insurance': insurance,
            'City': city,
            'Treatment_Cost': round(treatment_cost, 2),
            'Travel_Cost': round(travel_cost, 2),
            'Stay_Cost': round(stay_cost, 2),
            'Medicine_Cost': round(medicine_cost, 2),
            'Total_Cost': round(total_cost, 2)
        })
        
    df = pd.DataFrame(data)
    df.to_csv('dataset.csv', index=False)
    print("Dataset generated with 10,000 rows.")
    return df

def train_models():
    df = pd.read_csv('dataset.csv', keep_default_na=False)
    
    categorical_cols = ['Disease', 'Country', 'Hospital_Type', 'Travel_Class', 'Room_Type', 'Doctor_Experience', 'Insurance', 'City']
    numeric_features = ['Stay_Days']
    
    # Preprocessing Pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
        ])
    
    targets = ['Treatment_Cost', 'Travel_Cost', 'Stay_Cost', 'Medicine_Cost', 'Total_Cost']
    
    X = df[categorical_cols + numeric_features]
    Y = df[targets]
    
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    print("Training Pipeline Models...")
    
    # Extract unique categories for Streamlit UI dropdowns before saving
    unique_categories = {col: df[col].unique().tolist() for col in categorical_cols}
    joblib.dump(unique_categories, "models/categories.pkl")
    
    for target in targets:
        if target == 'Total_Cost':
            # XGBoost is great but let's stick to RandomForestRegressor for the pipeline to avoid version mismatch issues
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", model)
        ])
        
        pipeline.fit(X_train, y_train[target])
        preds = pipeline.predict(X_test)
        
        r2 = r2_score(y_test[target], preds)
        print(f"{target} Pipeline R2 Score: {r2:.4f}")
        
        joblib.dump(pipeline, f'models/{target.lower()}_pipeline.pkl')

if __name__ == '__main__':
    generate_dataset()
    train_models()
