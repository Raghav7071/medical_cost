import random

def get_hospitals(disease, country, city, budget):
    # Mock database logic
    base_hospitals = [
        {"Name": f"Global {city} Medical Center", "Rating": 4.8, "Specialization": disease, "City": city, "Cost_Range": "Premium"},
        {"Name": f"Care Hospital {city}", "Rating": 4.5, "Specialization": "Multispecialty", "City": city, "Cost_Range": "Standard"},
        {"Name": f"Advanced {disease} Institute", "Rating": 4.9, "Specialization": disease, "City": city, "Cost_Range": "Luxury"},
        {"Name": f"{country} National Health", "Rating": 4.2, "Specialization": "Multispecialty", "City": city, "Cost_Range": "Budget"}
    ]
    
    # Filter based on budget
    if budget < 5000:
        return [h for h in base_hospitals if h['Cost_Range'] in ['Budget', 'Standard']]
    elif budget < 15000:
        return [h for h in base_hospitals if h['Cost_Range'] in ['Standard', 'Premium']]
    else:
        return [h for h in base_hospitals if h['Cost_Range'] in ['Premium', 'Luxury']]

def get_doctors(disease, country):
    doctors = [
        {"Name": "Dr. Sarah Jenkins", "Experience": "15 Years", "Specialization": disease, "Language": "English, Spanish"},
        {"Name": "Dr. Amit Patel", "Experience": "20+ Years", "Specialization": disease, "Language": "English, Hindi"},
        {"Name": "Dr. Kenji Tanaka", "Experience": "10 Years", "Specialization": disease, "Language": "English, Japanese"},
        {"Name": "Dr. Elena Rossi", "Experience": "12 Years", "Specialization": disease, "Language": "English, Italian"}
    ]
    random.shuffle(doctors)
    return doctors[:2]

def compare_packages(disease):
    return {
        "Standard": {
            "Room": "Semi-Private",
            "Consultations": 2,
            "Airport_Transfer": "No",
            "Cost_Multiplier": 1.0
        },
        "Premium": {
            "Room": "Private",
            "Consultations": 5,
            "Airport_Transfer": "Yes",
            "Cost_Multiplier": 1.5
        },
        "Luxury": {
            "Room": "VIP Suite",
            "Consultations": "Unlimited",
            "Airport_Transfer": "Limousine",
            "Cost_Multiplier": 2.5
        }
    }
