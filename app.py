import streamlit as st
import joblib
import pickle
import pandas as pd
import numpy as np
from datetime import time
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Flight Price Predictor", layout="wide")

st.title("✈️ Flight Price Prediction App")
st.markdown("---")

# ========== PREPROCESSING FUNCTION ==========
def preprocess_input(input_df, label_encoders):
    """Preprocess input data to match training pipeline"""
    df = input_df.copy()
    
    # Convert Duration from total minutes to hours and minutes
    if 'Duration' in df.columns:
        total_minutes = int(df['Duration'].iloc[0])
        df['Dur_hour'] = total_minutes // 60
        df['Dur_min'] = total_minutes % 60
        df.drop('Duration', axis=1, inplace=True)
    
    # Rename Day to Date for consistency
    if 'Day' in df.columns:
        df.rename(columns={'Day': 'Date'}, inplace=True)
    
    # Create Arrival_month (from Month for simplicity)
    if 'Month' in df.columns and 'Arrival_month' not in df.columns:
        df['Arrival_month'] = df['Month'].iloc[0]
    
    # Rename arrival columns to match training
    if 'Arr_hour' in df.columns:
        df.rename(columns={'Arr_hour': 'Arrival_hour'}, inplace=True)
    if 'Arr_min' in df.columns:
        df.rename(columns={'Arr_min': 'Arrival_minute'}, inplace=True)
    
    # Rename route columns to match training (Route_1, Route_2, etc.)
    for i in range(1, 6):
        old_col = f"route{i}"
        new_col = f"Route_{i}"
        if old_col in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)
        else:
            # Add missing route columns with default value
            df[new_col] = 'None'
    
    # Ensure numeric columns
    numeric_cols = ['Dur_hour', 'Dur_min', 'Dep_hour', 'Dep_min', 'Arrival_hour', 
                    'Arrival_minute', 'Arrival_month', 'Date', 'Month', 'Year']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Ensure Total_Stops is string
    if 'Total_Stops' in df.columns:
        df['Total_Stops'] = df['Total_Stops'].astype(str).str.strip()
    
    # Apply label encoding to categorical columns
    for col in df.columns:
        if df[col].dtype == 'object' and col in label_encoders:
            le = label_encoders[col]
            # Handle unknown values by using the first class or -1
            df[col] = df[col].apply(
                lambda x: le.transform([str(x)])[0] if str(x) in le.classes_ else 0
            )
    
    # Apply one-hot encoding
    df_encoded = pd.get_dummies(df, drop_first=False)
    
    return df_encoded

# ========== LOAD MODEL & ARTIFACTS ==========
@st.cache_resource
def load_all():
    model = load_model("flight_model.keras", compile=False)
    
    # Load label encoders
    with open('label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)
    
    # Load feature columns
    with open('feature_columns.pkl', 'rb') as f:
        feature_columns = pickle.load(f)
    
    # Load training data for reference
    df = pd.read_excel("Data_Train.xlsx")
    
    # Clean Total_Stops: convert to string and remove NaNs
    df['Total_Stops'] = df['Total_Stops'].fillna('0')
    df['Total_Stops'] = df['Total_Stops'].astype(str).str.strip()
    
    # Remove any rows with NaN in key columns for selectbox options
    df_clean = df.dropna(subset=['Airline', 'Source', 'Destination', 'Additional_Info'])
    
    return model, label_encoders, feature_columns, df, df_clean

try:
    model, label_encoders, feature_columns, df, df_clean = load_all()

    st.sidebar.header("🛫 Enter Flight Details")

    airline = st.selectbox("Airline", sorted(df_clean["Airline"].unique()))
    source = st.selectbox("Source", sorted(df_clean["Source"].unique()))
    destination = st.selectbox("Destination", sorted(df_clean["Destination"].unique()))
    additional_info = st.selectbox("Additional Info", sorted(df_clean["Additional_Info"].unique()))
    
    # Handle Total_Stops - all strings now
    stops_options = sorted(set(df_clean["Total_Stops"].unique()))
    total_stops = st.selectbox("Total Stops", stops_options)

    duration = st.number_input("Duration (in minutes)", min_value=0, value=120)

    # Journey Date
    st.subheader("📅 Journey Date")
    col1, col2, col3 = st.columns(3)
    with col1:
        day = st.number_input("Day", min_value=1, max_value=31, value=15)
    with col2:
        month = st.number_input("Month", min_value=1, max_value=12, value=6)
    with col3:
        year = st.number_input("Year", min_value=2018, max_value=2025, value=2019)

    # Flight Times
    st.subheader("⏰ Flight Times")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Departure Time**")
        dep_time = st.time_input("When does the flight depart?", value=time(10, 30))
        dep_hour = dep_time.hour
        dep_min = dep_time.minute
    
    with col2:
        st.write("**Arrival Time**")
        arr_time = st.time_input("When does the flight arrive?", value=time(15, 45))
        arr_hour = arr_time.hour
        arr_min = arr_time.minute

    # Get unique routes from training data
    route_cols = [col for col in df.columns if col.startswith('Route_')]
    
    routes = {}
    cols_routes = st.columns(5)
    for i, col in enumerate(cols_routes):
        with col:
            if f'Route_{i+1}' in route_cols:
                route_options = sorted(df_clean[f'Route_{i+1}'].dropna().unique())
                if route_options:
                    routes[f'route{i+1}'] = st.selectbox(
                        f"Route {i+1}", 
                        route_options,
                        key=f"route_{i+1}"
                    )

    if st.button("💰 Predict Flight Price"):

        try:
            input_data = {
                "Airline": airline,
                "Source": source,
                "Destination": destination,
                "Total_Stops": total_stops,
                "Duration": duration,
                "Day": day,
                "Month": month,
                "Year": year,
                "Dep_hour": dep_hour,
                "Dep_min": dep_min,
                "Arr_hour": arr_hour,
                "Arr_min": arr_min,
                "Additional_Info": additional_info,
            }
            
            # Add routes
            input_data.update(routes)

            input_df = pd.DataFrame([input_data])

            # Preprocess the input
            input_encoded = preprocess_input(input_df, label_encoders)

            # Match feature columns
            input_encoded = input_encoded.reindex(columns=feature_columns, fill_value=0)

            # Make prediction
            prediction = model.predict(input_encoded, verbose=0)[0][0]

            st.markdown("---")
            st.subheader("📊 Prediction Result")
            st.success(f"💰 Estimated Flight Price: ₹ {max(int(prediction), 0)}")
            
            # Show input features for debugging
            with st.expander("📋 See input features (Debug)"):
                st.write(input_encoded.head())

        except Exception as pred_error:
            st.error(f"❌ Prediction Error: {pred_error}")

except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.info("Make sure the following files exist in the directory:")
    st.info("- flight_model.keras")
    st.info("- label_encoders.pkl")
    st.info("- feature_columns.pkl")
    st.info("- Data_Train.xlsx")