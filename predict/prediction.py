# prediction.py
import numpy as np
import pandas as pd
from catboost import CatBoostRegressor, Pool

def load_model():
    # Load the pre-trained CatBoost model
    model = CatBoostRegressor()
    model.load_model("model/catboost_model_with_tuning.cbm")
    return model

def prepare_input_data(features_df, merged_data, postal_code, municipality, property_type, property_subtype,
                       state_of_building, number_of_rooms, living_area,fully_equipped_kitchen, 
                       terrace, garden, number_of_facades, swimming_pool, lift):
    # Retrieve backend data for additional features
    backend_data = features_df.iloc[0]  # Example fallback data
    province = backend_data.get("Province", "Unknown")
    surface_area_plot = backend_data.get('Surface_area_plot_of_land',0)
    distance_to_brussels = backend_data.get('Distance_to_Brussels', 0)
    distance_to_airport = backend_data.get('Distance_to_Nearest_Airport', 0)
    total_income = backend_data.get('total_income', 0)
    employment_rate = backend_data.get('Employment Rate (%)', 0)
    unemployment_rate = backend_data.get('Unemployment Rate (%)', 0)
    population_density = backend_data.get('Population Density', 0)
    total_area = backend_data.get('Total_Area', 0)
    total_amenities = backend_data.get('Total_Amenities', 0)
    average_room_size = backend_data.get('Average_Room_Size', 0)
    amenities_ratio = backend_data.get('Amenities_Ratio', 0)
    airport_interaction = backend_data.get('Airport_Brussels_Interaction', 0)
    density_unemployment_ratio = backend_data.get('Density_Unemployment_Ratio', 0)
    region_cluster = backend_data.get('Region_Cluster', 0)

    # Log transformations (ensure safe handling for zero values)
    living_area_log = np.log(living_area) if living_area > 0 else 0
    total_area_log = np.log(total_area) if total_area > 0 else 0
    total_income_log = np.log(total_income) if total_income > 0 else 0

    # Prepare the input data as a DataFrame
    input_data = pd.DataFrame([{
        'Price': 0.0,
        'Locality': postal_code,
        'Type_of_Property': property_type,
        'Subtype_of_Property': property_subtype,
        'State_of_the_Building': state_of_building,
        'Number_of_Rooms': number_of_rooms,
        'Living_Area': living_area,
        'Fully_Equipped_Kitchen': fully_equipped_kitchen,
        'Terrace': terrace,
        'Garden': garden,
        'Surface_area_plot_of_land': surface_area_plot,
        'Number_of_Facades': number_of_facades,
        'Swimming_Pool': swimming_pool,
        'Lift': lift,
        'Municipality': municipality,
        'Province': province,
        'Distance_to_Brussels': distance_to_brussels,
        'Distance_to_Nearest_Airport': distance_to_airport,
        'total_income': total_income,
        'Employment Rate (%)': employment_rate,
        'Unemployment Rate (%)': unemployment_rate,
        'Population Density': population_density,
        'Total_Area': total_area,
        'Total_Amenities': total_amenities,
        'Average_Room_Size': average_room_size,
        'Amenities_Ratio': amenities_ratio,
        'Living_Area_log': living_area_log,
        'Total_Area_log': total_area_log,
        'total_income_log': total_income_log,
        'Airport_Brussels_Interaction': airport_interaction,
        'Density_Unemployment_Ratio': density_unemployment_ratio,
        'Region_Cluster': region_cluster
    }])

    # Ensure categorical features are strings
    cat_features = [
        'Locality', 'Type_of_Property', 'Subtype_of_Property',
        'State_of_the_Building', 'Fully_Equipped_Kitchen',
        'Terrace', 'Garden', 'Swimming_Pool', 'Lift',
        'Municipality', 'Province'
    ]
    input_data[cat_features] = input_data[cat_features].astype(str)
    
    return input_data, cat_features

def predict_price(model, input_data, cat_features):
    pool = Pool(input_data, cat_features=cat_features)
    prediction = model.predict(pool)
    return np.exp(prediction[0])  # Return price prediction
