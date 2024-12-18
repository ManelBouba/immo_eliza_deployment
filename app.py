import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from preprocessing.cleaning_data import load_data, get_unique_values
from predict.prediction import load_model, prepare_input_data, predict_price
from time import time

# Streamlit page configuration
st.set_page_config(page_title="🏠 House Price Predictor", page_icon="🏡", layout="wide")

# Caching the loading of the model and data
@st.cache_resource
def load_data_and_model():
    features_df, merged_data = load_data()
    locality_unique, property_type_unique, property_subtype_unique, state_of_building_unique = get_unique_values(features_df)
    model = load_model()
    return features_df, merged_data, locality_unique, property_type_unique, property_subtype_unique, state_of_building_unique, model

# Load resources
features_df, merged_data, locality_unique, property_type_unique, property_subtype_unique, state_of_building_unique, model = load_data_and_model()

# Custom CSS for Styling
st.markdown("""
<style>
/* Body Styling */
body {
    background-color: #e0f7fa;
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
}

/* Title and description */
.title {
    font-size: 48px;
    font-weight: bold;
    color: #00796b;
    text-align: center;
    padding-top: 40px;
    margin-bottom: 20px;
}

.description {
    font-size: 20px;
    color: #444;
    text-align: center;
    margin-bottom: 40px;
    line-height: 1.6;
}

/* Card Container */
.card {
    background: #ffffff;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.15);
}

/* Section Headers */
h4.centered-title {
    font-size: 26px;
    font-weight: bold;
    color: #00796b;
    margin-bottom: 10px;
    text-align: center;
}

/* Prediction Output Styling */
.output {
    font-size: 36px;
    color: #388e3c;
    font-weight: bold;
    text-align: center;
    margin-top: 30px;
    margin-bottom: 20px;
}

/* Button Styling */
.stButton>button {
    background-color: #00796b;
    color: white;
    font-size: 18px;
    border-radius: 12px;
    padding: 16px 24px;
    cursor: pointer;
    border: none;
    width: 100%;
    transition: background-color 0.3s ease, transform 0.3s ease;
}

.stButton>button:hover {
    background-color: #004d40;
    transform: translateY(-4px);
}

.stButton>button:active {
    background-color: #004d40;
    transform: translateY(0);
}

/* Input Fields */
.stInput input {
    height: 50px;
    font-size: 18px;
    padding-left: 10px;
    border-radius: 10px;
    border: 1px solid #ccc;
}

.stSelectbox, .stNumberInput {
    font-size: 18px;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #ccc;
}

/* Map Styling */
.st-folium {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* Footer and Disclaimer */
.footer {
    font-size: 14px;
    color: #888;
    text-align: center;
    margin-top: 50px;
    padding: 20px;
    background-color: #00796b;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<p class='title'>House Price Prediction</p>", unsafe_allow_html=True)
st.markdown("<p class='description'>Select a location, provide property details, and get a price estimate instantly!</p>", unsafe_allow_html=True)


# Map Section
st.markdown("<div class='card'><h4 class='centered-title'>📍 Select a Location</h4></div>", unsafe_allow_html=True)

# Optimized Map: Start with a zoomed-out view and limit markers
map_center = [50.8503, 4.3517]  # Center on Brussels
m = folium.Map(location=map_center, zoom_start=8)  # Start with a larger zoom level

# Initialize MarkerCluster to handle clustering
marker_cluster = MarkerCluster().add_to(m)

# Function to add markers based on the visible map bounds
def add_markers_in_bounds(start_lat, start_lon, end_lat, end_lon):
    """
    Add markers within the visible map bounds.
    """
    visible_data = merged_data[ 
        (merged_data['lat'] >= start_lat) & (merged_data['lat'] <= end_lat) & 
        (merged_data['lon'] >= start_lon) & (merged_data['lon'] <= end_lon)
    ]
    for _, row in visible_data.iterrows():
        folium.Marker(
            [row['lat'], row['lon']],
            popup=f"Postal Code: {row['postal_code']}<br>Municipality: {row['municipality']}",
            tooltip="Click to select this location",
        ).add_to(marker_cluster)

# Display the map with the clustering approach
st_map = st_folium(m, width=1400, height=450)

# Safely get the bounds of the visible map area after panning/zooming
bounds = st_map.get("bounds", None)

# Check if bounds are available and valid
if bounds and isinstance(bounds, list) and len(bounds) == 2:
    try:
        # Ensure the bounds have two valid lat/lon values
        start_lat, start_lon = bounds[0]
        end_lat, end_lon = bounds[1]
        
        # Add markers based on visible bounds
        add_markers_in_bounds(start_lat, start_lon, end_lat, end_lon)
    except Exception as e:
        # If an error occurs, do nothing (no warning message shown)
        pass
else:
    # If bounds are not available, use a default location without showing a warning
    default_lat, default_lon = 50.8503, 4.3517  # Brussels coordinates
    add_markers_in_bounds(default_lat - 0.1, default_lon - 0.1, default_lat + 0.1, default_lon + 0.1)

# Get clicked location from the map
clicked_location = st_map.get("last_clicked", None)

# Initialize address defaults
postal_code, municipality = None, None
if clicked_location:
    lat = clicked_location['lat']
    lon = clicked_location['lng']
    selected_row = merged_data.iloc[((merged_data['lat'] - lat) ** 2 + (merged_data['lon'] - lon) ** 2).idxmin()]
    postal_code = selected_row['postal_code']
    municipality = selected_row['municipality']
    province = selected_row['province']  

# Display selected address
if postal_code and municipality:
    st.markdown(f"**Selected Location:** {municipality}, {postal_code},{province}")
else:
    st.markdown("**Selected Location:** Please click on the map to select a location.")

# Property Details Section
st.markdown("<div class='card'><h4 class='centered-title'>🏠 Main Features</h4></div>", unsafe_allow_html=True)

# Main Features
col1, col2 = st.columns(2)
with col1:

    apartment_subtypes = [
        "PENTHOUSE", "APARTMENT", "APARTMENT_BLOCK", "DUPLEX", 
        "FLAT_STUDIO", "TRIPLEX", "GROUND_FLOOR", 
        "LOFT", "SERVICE_FLAT", "KOT"
    ]

    house_subtypes = [
        "HOUSE", "VILLA", "TOWN_HOUSE", "COUNTRY_COTTAGE", 
        "BUNGALOW", "MANSION", "CHALET", 
        "FARMHOUSE", "MANOR_HOUSE"
    ]

    # Property Type Dropdown
    property_type = st.selectbox("Type of Property", ["Apartment", "House"])

    # Dynamic Filtering Based on Property Type
    if property_type == "Apartment":
        filtered_subtypes = apartment_subtypes
    elif property_type == "House":
        filtered_subtypes = house_subtypes
    else:
        filtered_subtypes = ["MIXED_USE_BUILDING", "EXCEPTIONAL_PROPERTY", "OTHER_PROPERTY"]

    # Subtype Dropdown
    property_subtype = st.selectbox('Subtype of Property', filtered_subtypes)
    state_of_building = st.selectbox('State of the Building', state_of_building_unique)

with col2:
    
    number_of_facades = st.number_input('Number of Facades', min_value=1, max_value=4, step=1)
      # Define dynamic ranges based on Property Subtype
# Define dynamic ranges for Living Area based on Property Subtype
    if property_subtype in apartment_subtypes:
        living_area_min = 30.0  # Minimum Living Area for Apartment
        living_area_max = 150.0  # Maximum Living Area for Apartment
        number_of_rooms_min = 1  # Minimum number of rooms for Apartment
        number_of_rooms_max = 5  # Maximum number of rooms for Apartment
    elif property_subtype in house_subtypes:
        living_area_min = 100.0  # Minimum Living Area for House/Villa
        living_area_max = 500.0  # Maximum Living Area for House/Villa
        number_of_rooms_min = 3  # Minimum number of rooms for House/Villa
        number_of_rooms_max = 10  # Maximum number of rooms for House/Villa
    else:
        living_area_min = 50.0  # Default range for other properties
        living_area_max = 300.0
        number_of_rooms_min = 1
        number_of_rooms_max = 10

    # Living Area (now placed in the first column)
    living_area = st.number_input(
        'Living Area (sq. meters)', 
        min_value=living_area_min, 
        max_value=living_area_max, 
        step=1.0
    )

    # Number of Rooms (placed in the first column too)
    number_of_rooms = st.number_input(
        'Number of Rooms', 
        min_value=number_of_rooms_min, 
        max_value=number_of_rooms_max, 
        step=1
    )

# Extra Features
st.markdown("<div class='card'><h4 class='centered-title'>✨ Extra Features</h4></div>", unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    fully_equipped_kitchen = st.radio('Fully Equipped Kitchen', ['Yes', 'No'], horizontal=True)
    terrace = st.radio('Terrace', ['Yes', 'No'], horizontal=True)
with col4:
    garden = st.radio('Garden', ['Yes', 'No'], horizontal=True)
    swimming_pool = st.radio('Swimming Pool', ['Yes', 'No'], horizontal=True)

lift = st.radio('Lift', ['Yes', 'No'], horizontal=True)

# Convert Yes/No to binary for prediction
fully_equipped_kitchen = 1 if fully_equipped_kitchen == 'Yes' else 0
terrace = 1 if terrace == 'Yes' else 0
garden = 1 if garden == 'Yes' else 0
swimming_pool = 1 if swimming_pool == 'Yes' else 0
lift = 1 if lift == 'Yes' else 0

# Test MAE (Mean Absolute Error)
TEST_MAE = 48726.73  # Predefined MAE value

if st.button("🔮 Predict Price", use_container_width=True):
    if not (postal_code and municipality):
        st.warning("Please select a location from the map.")
    elif property_type is None or property_subtype is None or state_of_building is None or number_of_rooms is None or living_area is None:
        st.warning("Please complete all property details.")
    else:
        with st.spinner('🔄Calculating price...'):
            start_time = time()
            input_data, cat_features = prepare_input_data(features_df, merged_data, postal_code, municipality, 
                                                          property_type, property_subtype, state_of_building, 
                                                          number_of_rooms, living_area,
                                                          fully_equipped_kitchen, terrace, garden, 
                                                          number_of_facades, swimming_pool, lift)
            
            predicted_price = predict_price(model, input_data, cat_features)
            prediction_time = time() - start_time

            # Calculate Confidence Interval
            lower_bound = predicted_price - TEST_MAE
            upper_bound = predicted_price + TEST_MAE

            # Display Predicted Price with Confidence Interval
            st.markdown(f"""
            <p class='output'>
                Predicted Price: <strong>€{predicted_price:,.2f}</strong>
            </p>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <p class='description' style='color: #555;'>
                Confidence Interval: €{lower_bound:,.2f} - €{upper_bound:,.2f}
                <br>
                Calculation Time: {prediction_time:.2f} seconds
            </p>
            """, unsafe_allow_html=True)

            # Explain MAE and Prediction Variability
            st.markdown("""
            <div style="color: #777; text-align: center;">
                <p><strong>About the Prediction:</strong> The model's Mean Absolute Error (MAE) is €48,726.73, 
                which means that predictions typically deviate from the actual price by this amount on average.</p>
                <p>This confidence interval provides a range within which the actual price is likely to fall.</p>
            </div>
            """, unsafe_allow_html=True)

            # Disclaimer
            st.markdown("""
            <p class='description' style='color: #777;'>
                Note: This prediction is based on historical data and may not fully reflect current market trends.
            </p>
            """, unsafe_allow_html=True)

