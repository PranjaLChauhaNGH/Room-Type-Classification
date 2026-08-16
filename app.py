import streamlit as st
import requests

st.set_page_config(page_title="Airbnb Room Type Predictor", layout="centered")

st.title("Airbnb Room Type Predictor")
st.write("Provide the listing details below to predict the room type using your FastAPI backend and machine learning pipeline.")

with st.form("prediction_form"):
    st.subheader("Listing Details")
    
    neighbourhood_group = st.selectbox(
        "Neighbourhood Group",
        ['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx']
    )
    
    neighbourhood = st.text_input("Neighbourhood", value="Williamsburg")
    
    col1, col2 = st.columns(2)
    with col1:
        latitude = st.number_input("Latitude", value=40.7128, format="%.6f", min_value=-99.0, max_value=99.0)
        price = st.number_input("Price ($)", min_value=0.0, max_value=999.0, value=100.0)
        number_of_reviews = st.number_input("Number of Reviews", min_value=0, max_value=999, value=10)
        calculated_host_listings_count = st.number_input("Host Listings Count", min_value=0, max_value=99, value=1)
        
    with col2:
        longitude = st.number_input("Longitude", value=-74.0060, format="%.6f", min_value=-180.0, max_value=180.0)
        minimum_nights = st.number_input("Minimum Nights", min_value=0, max_value=99, value=1)
        reviews_per_month = st.number_input("Reviews Per Month", min_value=0, max_value=99, value=1)
        availability_365 = st.number_input("Availability (Days in a year)", min_value=0, max_value=365, value=30)

    submit_button = st.form_submit_button(label="Predict Room Type")

if submit_button:
    payload = {
        "neighbourhood_group": neighbourhood_group,
        "neighbourhood": neighbourhood,
        "latitude": latitude,
        "longitude": longitude,
        "price": price,
        "minimum_nights": minimum_nights,
        "number_of_reviews": number_of_reviews,
        "reviews_per_month": reviews_per_month,
        "calculated_host_listings_count": calculated_host_listings_count,
        "availability_365": availability_365
    }
    
    api_url = "http://127.0.0.1:8000/predict"
    
    try:
        with st.spinner("Connecting to FastAPI backend..."):
            response = requests.post(api_url, json=payload)
            
        if response.status_code == 200:
            result = response.json()
            st.metric(label="Predicted Room Type", value=result["Predicted_room_type"])
 
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")
            
    except requests.exceptions.ConnectionError:
        st.error("Failed to connect to the FastAPI server. Make sure your FastAPI backend is running via `uvicorn main:app --reload`.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")