# data_cleaned.py
import pandas as pd

def load_data():
    # Load the necessary datasets
    features_df = pd.read_csv('Data/immoweb_features2.csv')
    merged_data = pd.read_csv('Data/merged_coordinates_municipality_province.csv')
    
    return features_df, merged_data

def get_unique_values(features_df):
    # Extract unique values for input options
    locality_unique = features_df['Locality'].unique().tolist()
    property_type_unique = features_df['Type_of_Property'].unique().tolist()
    property_subtype_unique = features_df['Subtype_of_Property'].unique().tolist()
    state_of_building_unique = features_df['State_of_the_Building'].unique().tolist()
    
    return locality_unique, property_type_unique, property_subtype_unique, state_of_building_unique
