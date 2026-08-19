import streamlit as st
import requests

st.set_page_config(page_title="Airbnb Room Type Predictor", layout="centered")

st.title("Airbnb Room Type Predictor")

# Mapping of Neighbourhood Groups to non-zero Neighbourhoods
NEIGHBOURHOOD_MAP = {
    "Bronx": [
        "Allerton", "Baychester", "Belmont", "City Island", "Clason Point", "Concourse", 
        "Concourse Village", "Co-op City", "East Morrisania", "Eastchester", "Edenwald", 
        "Fieldston", "Fordham", "Highbridge", "Hunts Point", "Kingsbridge", "Longwood", 
        "Melrose", "Morris Heights", "Morris Park", "Morrisania", "Mott Haven", "Mount Eden", 
        "Mount Hope", "North Riverdale", "Norwood", "Olinville", "Parkchester", "Pelham Bay", 
        "Pelham Gardens", "Port Morris", "Riverdale", "Schuylerville", "Soundview", 
        "Spuyten Duyvil", "Throgs Neck", "Tremont", "University Heights", "Van Nest", 
        "Wakefield", "West Farms", "Westchester Square", "Williamsbridge", "Woodlawn"
    ],
    "Brooklyn": [
        "Bath Beach", "Bay Ridge", "Bedford-Stuyvesant", "Bensonhurst", "Bergen Beach", 
        "Boerum Hill", "Borough Park", "Brownsville", "Bushwick", "Canarsie", "Carroll Gardens", 
        "Clinton Hill", "Cobble Hill", "Coney Island", "Crown Heights", "Cypress Hills", 
        "Downtown Brooklyn", "DUMBO", "Dyker Heights", "East Flatbush", "East New York", 
        "Flatbush", "Flatlands", "Fort Greene", "Fort Hamilton", "Gowanus", "Gravesend", 
        "Greenpoint", "Kensington", "Midwood", "Navy Yard", "Park Slope", "Prospect Heights", 
        "Prospect-Lefferts Gardens", "Red Hook", "Sea Gate", "Sheepshead Bay", "South Slope", 
        "Sunset Park", "Vinegar Hill", "Williamsburg", "Windsor Terrace"
    ],
    "Manhattan": [
        "Battery Park City", "Chelsea", "Chinatown", "Civic Center", "East Harlem", 
        "East Village", "Financial District", "Flatiron District", "Gramercy", "Greenwich Village", 
        "Harlem", "Hell's Kitchen", "Inwood", "Kips Bay", "Little Italy", "Lower East Side", 
        "Manhattanville", "Midtown", "Morningside Heights", "Murray Hill", "NoHo", "Nolita", 
        "Roosevelt Island", "SoHo", "Stuyvesant Town", "Theater District", "Tribeca", 
        "Two Bridges", "Upper East Side", "Upper West Side", "Washington Heights", "West Village"
    ],
    "Queens": [
        "Arverne", "Astoria", "Bay Terrace", "Bayside", "Bayswater", "Belle Harbor", 
        "Bellerose", "Breezy Point", "Briarwood", "Cambria Heights", "College Point", "Corona", 
        "Ditmars Steinway", "Douglaston", "East Elmhurst", "Elmhurst", "Far Rockaway", 
        "Floral Park", "Flushing", "Forest Hills", "Fresh Meadows", "Glendale", "Hollis", 
        "Holliswood", "Howard Beach", "Jackson Heights", "Jamaica", "Jamaica Estates", 
        "Jamaica Hills", "Kew Gardens", "Kew Gardens Hills", "Laurelton", "Little Neck", 
        "Long Island City", "Maspeth", "Middle Village", "Ozone Park", "Queens Village", 
        "Rego Park", "Richmond Hill", "Ridgewood", "Rockaway Beach", "Rosedale", "South Ozone Park", 
        "Springfield Gardens", "Sunnyside", "Whitestone", "Woodhaven", "Woodside"
    ],
    "Staten Island": [
        "Arden Heights", "Arrochar", "Bay Terrace, Staten Island", "Bull's Head", "Castleton Corners", 
        "Clifton", "Concord", "Dongan Hills", "Eltingville", "Emerson Hill", "Fort Wadsworth", 
        "Graniteville", "Grant City", "Grymes Hill", "Howland Hook", "Huguenot", "Lighthouse Hill", 
        "Mariners Harbor", "Midland Beach", "New Brighton", "New Dorp", "New Dorp Beach", 
        "New Springville", "Oakwood", "Port Richmond", "Prince's Bay", "Randall Manor", 
        "Richmondtown", "Rosebank", "Rossville", "Shore Acres", "Silver Lake", "South Beach", 
        "St. George", "Stapleton", "Todt Hill", "Tompkinsville", "Tottenville", "Travis", 
        "West Brighton", "Westerleigh", "Willowbrook", "Woodrow"
    ]
}

st.subheader("Listing Details")

neighbourhood_group = st.selectbox(
    "Neighbourhood Group",
    options=list(NEIGHBOURHOOD_MAP.keys())
)

available_neighbourhoods = NEIGHBOURHOOD_MAP.get(neighbourhood_group, [])

neighbourhood = st.selectbox(
    "Neighbourhood",
    options=available_neighbourhoods
)

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

# Changed from st.form_submit_button to a standard st.button
submit_button = st.button(label="Predict Room Type")

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
    
    api_url = "https://room-type-classification-1.onrender.com/predict"
    
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
