import streamlit as st
import pandas as pd
from dashboard import create_dashboard
from predictionmodel import create_prediction_model
from home import create_home_page

# Set the page details at the very beginning of your script
st.set_page_config(
    page_title="Crop Price Prediction App",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="auto",  # Change sidebar state as desired
)
class SessionState:
    def __init__(self):
        self.selected_page = None

# Create a session state object
session_state = SessionState()

# Load your dataset (replace 'your_dataset.csv' with the actual file path)
df = pd.read_csv('wholesale_dataset.csv', usecols=[
    'date', 'regional', 'district', 'market', 'latitude', 'longitude',
    'category', 'commodity', 'unit', 'priceflag', 'pricetype', 'currency',
    'price', 'usdprice', 'year', 'month'
])

# Load the local CSS file for custom styling
st.markdown('<style>{}</style>'.format(open('style.css').read()), unsafe_allow_html=True)

# Add a rectangular image to the sidebar with a custom CSS class
logo = st.sidebar.image('logoo.PNG', use_column_width=True, caption="Empowering Agriculture with Data")

st.sidebar.markdown("---")

# Create buttons for navigation
selected_page = st.sidebar.radio("Select a Page", ["🏠 Home", "📊 Dashboard", "🔮 Prediction Model"])

# Conditional rendering based on the selected page
if selected_page == "📊 Dashboard":
    create_dashboard(df)
elif selected_page == "🔮 Prediction Model":
    create_prediction_model()
elif selected_page == "🏠 Home":
    create_home_page() 


# Add a footer with a copyright notice
st.sidebar.markdown("---")
st.sidebar.text("© 2023 dLab Tanzania")
