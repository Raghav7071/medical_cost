import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# Create saved_models directory if it doesn't exist
os.makedirs('saved_models', exist_ok=True)

# 1. Dataset Generation
def generate_synthetic_data(num_rows=5000):
    print("Generating synthetic dataset...")
    np.random.seed(42)
    
    diseases = ['Heart Bypass', 'Knee Replacement', 'Spinal Fusion', 'Cataract Surgery', 'Dental Implants', 'Cosmetic Surgery', 'Oncology Treatment']
    countries = ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'UAE']
    hospital_types = ['Public', 'Private', 'Premium International']
    treatment_types = ['Surgical', 'Non-Surgical', 'Radiotherapy', 'Chemotherapy']
    cities = ['Bangkok', 'Istanbul', 'Mumbai', 'Singapore', 'Kuala Lumpur', 'Dubai', 'Seoul']
    room_types = ['General Ward', 'Semi-Private', 'Private', 'VIP Suite']
    
    data = []
    
    for _ in range(num_rows):
        disease = np.random.choice(diseases)
        country = np.random.choice(countries)
        hospital_type = np.random.choice(hospital_types)
        treatment_type = np.random.choice(treatment_types)
        city = np.random.choice(cities)
        room_type = np.random.choice(room_types)
        
        # Base days depend on treatment
        stay_days = np.random.randint(1, 30)
        if disease in ['Heart Bypass', 'Spinal Fusion']:
            stay_days = np.random.randint(7, 45)
            
        # Cost generation logic based on combinations
        # Base treatment cost
        treatment_cost = np.random.uniform(2000, 15000)
        if disease == 'Heart Bypass': treatment_cost *= 3
        elif disease == 'Oncology Treatment': treatment_cost *= 4
        elif disease == 'Dental Implants': treatment_cost *= 0.5
        
        if hospital_type == 'Premium International': treatment_cost *= 1.8
        elif hospital_type == 'Private': treatment_cost *= 1.3
        
        # Travel expense
        travel_expense = np.random.uniform(500, 3000)
        if country in ['USA', 'Canada']: travel_expense *= 1.5
        
        # Stay cost
        daily_room_rate = 100
        if room_type == 'Semi-Private': daily_room_rate = 200
        elif room_type == 'Private': daily_room_rate = 400
        elif room_type == 'VIP Suite': daily_room_rate = 1000
        
        if city in ['Singapore', 'Dubai', 'Seoul']: daily_room_rate *= 1.5
        
        stay_cost = daily_room_rate * stay_days
        
        # Add some noise
        treatment_cost += np.random.normal(0, treatment_cost * 0.05)
        travel_expense += np.random.normal(0, travel_expense * 0.05)
        stay_cost += np.random.normal(0, stay_cost * 0.05)
        
        total_cost = treatment_cost + travel_expense + stay_cost
        
        data.append({
            'Disease': disease,
            'Country': country,
            'Hospital_Type': hospital_type,
            'Treatment_Type': treatment_type,
            'Stay_Days': stay_days,
            'City': city,
            'Room_Type': room_type,
            'Treatment_Cost': round(treatment_cost, 2),
            'Travel_Expense': round(travel_expense, 2),
            'Stay_Cost': round(stay_cost, 2),
            'Total_Cost': round(total_cost, 2)
        })
        
    df = pd.DataFrame(data)
    
    # Introduce some missing values to demonstrate missing value handling
    # We will randomly set 1% of values in numerical columns to NaN
    for col in ['Stay_Days', 'Treatment_Cost', 'Travel_Expense', 'Stay_Cost', 'Total_Cost']:
        mask = np.random.rand(len(df)) < 0.01
        df.loc[mask, col] = np.nan
        
    df.to_csv('dataset.csv', index=False)
    print("Dataset saved to dataset.csv")
    return df

def train_and_evaluate():
    print("Loading and preprocessing data...")
    df = pd.read_csv('dataset.csv')
    
    # Missing Value Handling
    # Fill numeric features with median
    numeric_cols = ['Stay_Days', 'Treatment_Cost', 'Travel_Expense', 'Stay_Cost', 'Total_Cost']
    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)
        
    # Features and Targets
    categorical_cols = ['Disease', 'Country', 'Hospital_Type', 'Treatment_Type', 'City', 'Room_Type']
    X = df[categorical_cols + ['Stay_Days']].copy()
    
    targets = ['Treatment_Cost', 'Travel_Expense', 'Stay_Cost', 'Total_Cost']
    Y = df[targets]
    
    # Label Encoding for categorical columns to keep models simple (One Hot Encoding can increase dimensionality a lot)
    # The user asked for both Label Encoding and One Hot Encoding. Let's use Label Encoding for high cardinality and OneHot for others, or just OneHot.
    # We will use One-Hot Encoding for training since it is generally better for RandomForest on categorical, 
    # but let's stick to a mix or just OneHot using pandas get_dummies, or scikit-learn OneHotEncoder.
    # Since we need to save the encoder for new data, we'll use a dictionary of LabelEncoders for simplicity.
    
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
        
    joblib.dump(label_encoders, 'saved_models/label_encoders.pkl')
    
    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, 'saved_models/scaler.pkl')
    
    models = {}
    metrics = {}
    
    print("Training models...")
    for target in targets:
        print(f"Training RandomForestRegressor for {target}...")
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train_scaled, y_train[target])
        
        # Predictions
        preds = rf.predict(X_test_scaled)
        
        # Evaluation
        mae = mean_absolute_error(y_test[target], preds)
        mse = mean_squared_error(y_test[target], preds)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test[target], preds)
        
        metrics[target] = {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'R2': r2
        }
        
        # Save model
        joblib.dump(rf, f'saved_models/rf_model_{target.lower()}.pkl')
        models[target] = rf
        
    # Print metrics
    print("\nModel Evaluation Metrics:")
    for target, metric in metrics.items():
        print(f"\nTarget: {target}")
        print(f"  MAE: {metric['MAE']:.2f}")
        print(f"  MSE: {metric['MSE']:.2f}")
        print(f"  RMSE: {metric['RMSE']:.2f}")
        print(f"  R2 Score: {metric['R2']:.4f}")
        
    # Save metrics
    joblib.dump(metrics, 'saved_models/metrics.pkl')
    print("\nAll models and preprocessors saved to saved_models/ directory.")

if __name__ == "__main__":
    generate_synthetic_data()
    train_and_evaluate()
