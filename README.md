# House Price Prediction Project

This project predicts house prices based on various property features such as location, property type, and amenities. It uses machine learning algorithms to train a model on historical property data, and then allows users to predict house prices by inputting property details.

## Project Structure
```plaintext
immo_eliza_deployment/
├── app.py                                           # The main Streamlit application that interacts with the user. 
├── Data/                                            # Contains datasets used for the project.
│   ├── immoweb_features2.csv                        # A CSV file with property features like property type, municipality.
│   ├── merged_coordinates_municipality_province.csv # A merged CSV file with coordinates  municipality and proviance data.
├── model/                                           # Contains the trained machine learning model.
│   └── catboost_model_with_tuning.cbm               # The trained model for predicting house prices
├── preprocessing/                                   # Contains the code for cleaning and preparing the data.
│   ├── cleaning_data.py                             # Scripts for cleaning and preprocessing data
├── predict/                                         # Contains the code responsible for making predictions
│   ├── prediction.py                                # Contains the logic to load the trained model and make predictions.
├── runtime.txt                                      # Python version specification (python-3.11)
└── requirements.txt                                 # A list of Python dependencies required to run the project.
```
## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ManelBouba/immo_eliza_deployment.git
   cd immo_eliza_deployment
   ```
2. **Install dependencies**:It is recommended to use a virtual environment. You can install all the required dependencies using pip:
   ```bash
    pip install -r requirements.txt
    ```
3. **Download or train the model**:If you don't have the pre-trained model (`catboost_model_with_tuning.cbm`), you can train it using the provided scripts in the `predict` folder.

4. **Run the application**:To start the Streamlit app, run:
   ```bash
    streamlit run app.py
    ```
## How It Works
1. **Data Preprocessing**:

- The data is preprocessed and cleaned using the scripts in the `preprocessing` folder. The `cleaning_data.py` script removes any missing or inconsistent data points.

2. **Model Training**:

- The machine learning model is trained using the preprocessed data. The model is stored in `catboost_model_with_tuning.cbm`  . It uses various features like property type, number of rooms, and location to predict the price of a property.

3. **Prediction**:

- The `predict` folder contains logic for making predictions using the trained model. The input data is prepared using the `prepare_input_data` function, and the `predict_price` function makes the prediction based on the user's input.

4. **App**:

- The `app.py` file is the user-facing application built with Streamlit. Users can select a location on the map, enter property details like the number of rooms, property type, and amenities, and receive an estimated house price.

## Features

- Location-based Prediction: The app allows users to select a location using a map and get predictions based on that location's postal code and municipality.
  
- Detailed Property Information: Users can input various details like the number of rooms, property type, state of the building, and more.
  
- Model-based Price Estimation: The app uses a machine learning model trained on historical property data to predict house prices.

## Usage
1. Select a location: You can either click on the map to select a location or use the default location.
   
2. Enter property details: Provide property details such as type, state of the building, number of rooms, living area, and additional features like a garden or swimming pool.
   
3. Predict Price: Once you've filled in the required details, click the "Predict Price" button to get the predicted house price.
   
## Example of Prediction

After selecting a location and providing property details, you will see a predicted price based on the model. For example:
   ```yaml
    **Selected Location:** saint-gilles, 1060,Brussels Capital
     Predicted Price: €551,102.88
   ```

## Development

If you want to contribute to the project, follow these steps:

1. Fork the repository and clone it to your local machine.

2. Create a new branch for your feature or bug fix.
   
3. Implement your changes.
   
4. Run tests to make sure everything works as expected.
   
5. Submit a pull request.
