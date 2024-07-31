import streamlit as st
from streamlit_option_menu import option_menu
import joblib
import warnings
import pandas as pd
import plotly.express as px
from io import StringIO
import requests
import streamlit_lottie as st_lottie


# Load models
maternal_model = joblib.load(open("maternal_model.sav", 'rb'))
fetal_model = joblib.load(open("fetal_health_classifier.sav", 'rb'))

# Page config
st.set_page_config(page_title="MedCare", page_icon="🏥", layout="wide")

# Define CSS for light and dark modes
light_mode_css = """
<style>
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    .stSidebar {
        background-color: #F0F2F6;
    }
    .stButton>button {
        color: #000000;
        background-color: #FFFFFF;
        border: 1px solid #000000;
    }
</style>
"""

dark_mode_css = """
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stSidebar {
        background-color: #262730;
    }
    .stButton>button {
        color: #FAFAFA;
        background-color: #262730;
        border: 1px solid #FAFAFA;
    }
</style>
"""
# Sidebar
with st.sidebar:
    st.title("MedPredict")
    st.write("Welcome to MedCare")
    
    # Dark mode toggle
    dark_mode = st.checkbox("Dark Mode", value=False)
    
    selected = option_menu('Menu',
                           ['About us',
                            'Pregnancy Risk Prediction',
                            'Fetal Health Prediction',
                            'Dashboard'],
                           icons=['info-circle', 'heart', 'activity', 'graph-up'],
                           default_index=0)

# Apply the appropriate CSS based on dark mode selection
if dark_mode:
    st.markdown(dark_mode_css, unsafe_allow_html=True)
else:
    st.markdown(light_mode_css, unsafe_allow_html=True)
# Helper function to load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# About Us
if selected == 'About us':
    st.title("Welcome to MedCare")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write(
            "At MedCare, our mission is to revolutionize healthcare by offering innovative solutions through predictive analysis. "
            "Our platform is specifically designed to address the intricate aspects of maternal and fetal health, providing accurate "
            "predictions and proactive risk management."
        )
    
    with col2:
        lottie_health = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5njp3vgg.json")
        st_lottie.st_lottie(lottie_health, height=200)
    
    st.header("Our Features")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.subheader("1. Pregnancy Risk Prediction")
        st.image("Maternal Health.png", use_column_width=True)
        st.write("Analyze various parameters to predict potential risks during pregnancy.")
    
    with feature_col2:
        st.subheader("2. Fetal Health Prediction")
        st.image("Fetal Health.png", use_column_width=True)
        st.write("Assess fetal health status using advanced algorithms and comprehensive data analysis.")
    
    #with feature_col3:
     #   st.subheader("3. Interactive Dashboard")
      #  st.image("graphics/dashboard_image.jpg", use_column_width=True)
       # st.write("Monitor and manage health data with our user-friendly interface.")

# Pregnancy Risk Prediction
elif selected == 'Pregnancy Risk Prediction':
    st.title('Pregnancy Risk Prediction')
    
    st.info("Predict pregnancy risks by analyzing parameters such as age, blood sugar levels, and blood pressure.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input('Age', min_value=0, max_value=100, value=30)
        diastolicBP = st.number_input('Diastolic BP (mmHg)', min_value=0, max_value=200, value=80)
        BS = st.number_input('Blood glucose (mmol/L)', min_value=0.0, max_value=20.0, value=5.0, step=0.1)
    
    with col2:
        bodyTemp = st.number_input('Body Temperature (°C)', min_value=35.0, max_value=42.0, value=37.0, step=0.1)
        heartRate = st.number_input('Heart rate (bpm)', min_value=40, max_value=200, value=75)
    
    if st.button('Predict Pregnancy Risk', key='predict_pregnancy'):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            predicted_risk = maternal_model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])
        
        risk_level = ["Low Risk", "Medium Risk", "High Risk"][predicted_risk[0]]
        risk_color = ["green", "orange", "red"][predicted_risk[0]]
        
        st.markdown(f"<h3 style='text-align: center; color: {risk_color};'>Risk Level: {risk_level}</h3>", unsafe_allow_html=True)
        
        # Add a progress bar to visualize the risk level
        st.progress(predicted_risk[0] / 2)  # Divide by 2 since we have 3 levels (0, 1, 2)

# Fetal Health Prediction
elif selected == 'Fetal Health Prediction':
    st.title('Fetal Health Prediction')
    
    st.info("Predict fetal health using Cardiotocogram (CTG) data.")
    
    # Create two columns for input fields
    col1, col2 = st.columns(2)
    
    # Dictionary to store input values
    inputs = {}
    
    # Input fields
    with col1:
        inputs['BaselineValue'] = st.number_input('Baseline Value', value=120.0)
        inputs['Accelerations'] = st.number_input('Accelerations', value=0.0)
        inputs['fetal_movement'] = st.number_input('Fetal Movement', value=0.0)
        inputs['uterine_contractions'] = st.number_input('Uterine Contractions', value=0.0)
        inputs['light_decelerations'] = st.number_input('Light Decelerations', value=0.0)
    
    with col2:
        inputs['severe_decelerations'] = st.number_input('Severe Decelerations', value=0.0)
        inputs['prolongued_decelerations'] = st.number_input('Prolongued Decelerations', value=0.0)
        inputs['abnormal_short_term_variability'] = st.number_input('Abnormal Short Term Variability', value=73.0)
        inputs['mean_value_of_short_term_variability'] = st.number_input('Mean Value Of Short Term Variability', value=0.5)
        inputs['percentage_of_time_with_abnormal_long_term_variability'] = st.number_input('Percentage Of Time With ALTV', value=43.0)
    
    # Additional input fields (you can add more as needed)
    inputs['mean_value_of_long_term_variability'] = 10.0
    inputs['histogram_width'] = 64.0
    inputs['histogram_min'] = 62.0
    inputs['histogram_max'] = 126.0
    inputs['histogram_number_of_peaks'] = 2.0
    inputs['histogram_number_of_zeroes'] = 0.0
    inputs['histogram_mode'] = 120.0
    inputs['histogram_mean'] = 137.0
    inputs['histogram_median'] = 121.0
    inputs['histogram_variance'] = 73.0
    inputs['histogram_tendency'] = 1.0
    
    if st.button('Predict Fetal Health', key='predict_fetal'):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            predicted_health = fetal_model.predict([list(inputs.values())])
        
        health_status = ["Normal", "Suspect", "Pathological"][predicted_health[0]]
        health_color = ["green", "orange", "red"][predicted_health[0]]
        
        st.markdown(f"<h3 style='text-align: center; color: {health_color};'>Fetal Health Status: {health_status}</h3>", unsafe_allow_html=True)
        
        # Add a gauge chart to visualize the health status
        fig = px.pie(values=[1], names=[health_status], color_discrete_sequence=[health_color], hole=0.7)
        fig.update_layout(annotations=[dict(text=health_status, x=0.5, y=0.5, font_size=20, showarrow=False)])
        st.plotly_chart(fig)

# Dashboard
elif selected == 'Dashboard':
    st.title('Maternal Health Dashboard')
    
    # You can add your dashboard implementation here
    # For example, you could display some charts or statistics
    
    st.write("This dashboard provides an overview of maternal health statistics.")
    
    # Sample data (replace with your actual data)
    data = {
        'Age Group': ['18-25', '26-35', '36-45', '46+'],
        'Low Risk': [30, 40, 20, 10],
        'Medium Risk': [15, 25, 30, 20],
        'High Risk': [5, 10, 15, 25]
    }
    
    df = pd.DataFrame(data)
    # Plotly Dark
    fig = px.bar(df, x='Age Group', y=['Low Risk', 'Medium Risk', 'High Risk'], 
             title='Pregnancy Risk Distribution by Age Group',
             labels={'value': 'Number of Pregnancies', 'variable': 'Risk Level'},
             color_discrete_map={'Low Risk': 'green', 'Medium Risk': 'orange', 'High Risk': 'red'},
             template='plotly_dark' if dark_mode else 'plotly')
    # Create a stacked bar chart
    fig = px.bar(df, x='Age Group', y=['Low Risk', 'Medium Risk', 'High Risk'], 
                 title='Pregnancy Risk Distribution by Age Group',
                 labels={'value': 'Number of Pregnancies', 'variable': 'Risk Level'},
                 color_discrete_map={'Low Risk': 'green', 'Medium Risk': 'orange', 'High Risk': 'red'})
    
    st.plotly_chart(fig)
    


# Add a footer
st.markdown("---")
st.markdown("© 2024 MedCare. All rights reserved.")