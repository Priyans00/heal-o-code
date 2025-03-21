import streamlit as st
import requests
from streamlit_qrcode_scanner import qrcode_scanner

API_URL = "http://127.0.0.1:5000"

st.title("QR Scanner for Meals Check-in")

if "qr_data" not in st.session_state:
    st.session_state.qr_data = None

meal_type = st.selectbox("Select Meal Type", ["dinner", "breakfast", "entry", "snacks"])

if "last_meal_type" not in st.session_state or st.session_state.last_meal_type != meal_type:
    st.session_state.qr_data = None
    st.session_state.last_meal_type = meal_type

qr_data = qrcode_scanner()

if qr_data:
    st.session_state.qr_data = qr_data 
if st.session_state.qr_data:
    st.success(f"Scanned QR Data: {st.session_state.qr_data}")
    print(f"Sending QR Data: {st.session_state.qr_data}")  
    
    response = requests.post(f"{API_URL}/{meal_type}", json={"srn": st.session_state.qr_data})

    if response.status_code == 200:
        data = response.json()
        st.write("✅ Response:", data)
    else:
        st.error("❌ Error sending data. Try again!")
        print(f"Error response: {response.status_code}, {response.text}")  
