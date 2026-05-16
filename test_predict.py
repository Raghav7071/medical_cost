import pandas as pd
import joblib

models = {
    'Treatment_Cost': joblib.load('models/treatment_cost_pipeline.pkl')
}

input_df = pd.DataFrame([{
    "Disease": "Oncology",
    "Country": "USA",
    "Hospital_Type": "Private",
    "Stay_Days": 10,
    "Travel_Class": "Economy",
    "Room_Type": "Private",
    "Doctor_Experience": "1-5 Years",
    "Insurance": "Full",
    "City": "New York"
}])

print("Dataframe columns:", input_df.columns.tolist())
try:
    pred = models['Treatment_Cost'].predict(input_df)
    print("Prediction:", pred)
except Exception as e:
    print("Error:", str(e))
