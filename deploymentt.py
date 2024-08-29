import streamlit as st
import joblib
import numpy as np
import pandas as pd
import pickle

# Load the compressed model and preprocessor
model = joblib.load('model_compressed.pkl')
preprocessor = joblib.load('preprocessor_compressed.pkl')

# Set page configuration and title
st.set_page_config(page_title="Life Expectancy Predictor", page_icon="🌍", layout="wide")

# Set the title of the app
st.title("🌍 Life Expectancy Prediction")

# Description
st.markdown("""
    ### Enter the details to predict life expectancy:
    This app uses various health, economic, and demographic factors to estimate the life expectancy in a given country. 
    Fill out the fields below and click **Predict** to get an estimate.
    """)

# Add a separator
st.markdown("---")

# Create user input fields using columns for a cleaner layout
with st.form("life_expectancy_form"):
    # First row of inputs
    col1, col2, col3 = st.columns(3)
    with col1:
        status = st.selectbox("Country Status", ["Developed", "Developing"])
        alcohol = st.number_input("Alcohol Consumption (liters)", min_value=0.0, max_value=20.0, step=0.1)
        adult_mortality = st.number_input("Adult Mortality (per 1000)", min_value=0, max_value=1000)
        measles = st.number_input("Measles Cases (per 1000)", min_value=0, max_value=1000)

    with col2:
        Reigon = st.selectbox("Region", ['Europe', 'Africa', 'Oceania', 'Asia', 'North America', 'South America'])
        percentage_expenditure = st.number_input("Percentage Expenditure on Health (%)", min_value=0.0, step=0.1)
        infant_deaths = st.number_input("Infant Deaths (per 1000)", min_value=0, max_value=1000)
        bmi = st.number_input("Average BMI", min_value=0.0, max_value=100.0, step=0.1)

    with col3:
        schooling = st.number_input("Schooling (years)", min_value=0.0, max_value=20.0, step=0.1)
        income_composition = st.number_input("Income Composition of Resources (index 0 to 1)", min_value=0.0, max_value=1.0, step=0.01)
        gdp = st.number_input("GDP per Capita (USD)", min_value=0.0, step=1.0)
        population = st.number_input("Population", min_value=0)
    # Second row of inputs
    col4, col5, col6 = st.columns(3)
    with col4:
        hepatitis_b = st.slider("Hepatitis B Immunization Coverage (%)", 0, 100)
        polio = st.slider("Polio Immunization Coverage (%)", 0, 100)
        diphtheria = st.slider("Diphtheria Immunization Coverage (%)", 0, 100)

    with col5:
        under_five_deaths = st.number_input("Under-five Deaths (per 1000)", min_value=0, max_value=1000)
        hiv_aids = st.number_input("HIV/AIDS Deaths (per 1000)", min_value=0, max_value=1000)
        total_expenditure = st.number_input("Total Health Expenditure (%)", min_value=0.0, step=0.1)

    with col6:
        thinness_1_19_years = st.number_input("Thinness (Ages 10-19) (%)", min_value=0.0, step=0.1)
        thinness_5_9_years = st.number_input("Thinness (Ages 5-9) (%)", min_value=0.0, step=0.1)

    # Create a button to predict life expectancy
    submit_button = st.form_submit_button("Predict Life Expectancy")

if submit_button:
    # Organize the input data
    input_data = pd.DataFrame({
        'Status': [status],
        'Region': [Reigon],
        'Adult Mortality': [adult_mortality],
        'infant deaths': [infant_deaths],
        'Alcohol': [alcohol],
        'percentage expenditure': [percentage_expenditure],
        'Hepatitis B': [hepatitis_b],
        'Measles ': [measles],
        ' BMI ': [bmi],
        'under-five deaths ': [under_five_deaths],
        'Polio': [polio],
        'Total expenditure': [total_expenditure],
        'Diphtheria ': [diphtheria],
        ' HIV/AIDS': [hiv_aids],
        'GDP': [gdp],
        'Population': [population],
        ' thinness  1-19 years': [thinness_1_19_years],
        ' thinness 5-9 years': [thinness_5_9_years],
        'Income composition of resources': [income_composition],
        'Schooling': [schooling]
    })

    # Preprocess the input data
    processed_data = preprocessor.transform(input_data)

    # Predict using the loaded model
    prediction = model.predict(processed_data)

    # Display the result in a well-styled card
    st.markdown("### Prediction Result:")
    st.success(f"The predicted life expectancy is: **{prediction[0]:.2f} years**")
    
    # Additional info
    st.markdown("🔍 *This prediction is based on data from various health and demographic sources.*")
