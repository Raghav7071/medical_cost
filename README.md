# AI-Powered Medical Tourism Cost Predictor

## 🏥 Project Overview
The AI-Powered Medical Tourism Cost Predictor is a comprehensive, machine learning-driven web application designed to help patients estimate the cost of medical procedures abroad. By considering factors such as the patient's condition, destination country, hospital type, and duration of stay, the platform provides highly accurate estimates for treatment, travel, and stay costs.

## ✨ Features
- **Accurate Cost Prediction**: Powered by a trained `RandomForestRegressor`, providing robust estimates.
- **Detailed Budget Breakdown**: Separate predictions for Treatment Cost, Travel Expense, and Hospital Stay Cost.
- **Modern UI**: A responsive, clean, and interactive interface built with Streamlit and styled with modern CSS.
- **Currency Conversion**: Easily switch between USD, INR, AED, EUR, and GBP.
- **PDF Report Generation**: Download detailed budget reports.
- **Data Analytics Dashboard**: Visualize historical data, healthcare distributions, and cost trends globally.
- **AI Recommendations**: Smart hospital and best city recommendations tailored to your selected medical procedure.
- **AI Chatbot**: Built-in assistant to answer simple queries about medical tourism.

## 🛠 Technologies Used
- **Frontend**: Streamlit, HTML/CSS
- **Backend**: Python 3
- **Machine Learning**: Scikit-learn, Pandas, Numpy, Joblib
- **Data Visualization**: Matplotlib
- **Document Generation**: ReportLab

## 📁 Project Structure
```
Medical_to/
├── app.py                  # Main Streamlit application
├── model_training.py       # Script for data generation and ML training
├── dataset.csv             # Synthetic healthcare dataset (Generated)
├── requirements.txt        # Python dependencies
├── saved_models/           # Directory for trained models and encoders
│   ├── rf_model_treatment_cost.pkl
│   ├── rf_model_travel_expense.pkl
│   ├── rf_model_stay_cost.pkl
│   ├── rf_model_total_cost.pkl
│   ├── label_encoders.pkl
│   └── scaler.pkl
├── utils/                  # Helper functions
│   └── helpers.py          # PDF generation & Currency conversion
└── assets/                 # Images, logos, and UI assets
```

## 🚀 Installation Steps

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd Medical_to
   ```

2. **Create a virtual environment (Optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate Data and Train the Model**:
   ```bash
   python model_training.py
   ```
   *This will generate the `dataset.csv` file with 5000 records and train the random forest models, saving them to the `saved_models/` folder.*

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 📸 Screenshots
*(Add your screenshots here)*
- **Cost Predictor Dashboard**
- **Data Analytics Visualization**
- **AI Recommendations and Report Download**

## 🌐 Deployment Instructions

### Deploying on Streamlit Cloud
1. Push this project to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub account and select this repository.
4. Set the main file path to `app.py`.
5. Click **Deploy**. Your app will be live in minutes.

### Deploying on Render or Hugging Face Spaces
- Ensure `requirements.txt` is present at the root.
- For Hugging Face Spaces, create a new Space, choose Streamlit as the SDK, and upload all files.

## 🔮 Future Enhancements
- Integrate a large language model (LLM) API like OpenAI for more dynamic chatbot capabilities.
- Add OCR for medical reports to auto-fill patient symptoms and disease suggestions.
- Live API integration for real-time currency conversion rates.
- Expand the dataset to include real-world hospital pricing APIs.
