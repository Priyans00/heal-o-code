import streamlit as st
import requests
from streamlit_qrcode_scanner import qrcode_scanner

API_URL = "https://heal-o-code.vercel.app"

st.title("QR Scanner for Meals Check-in")

if "qr_data" not in st.session_state:
    st.session_state.qr_data = None
if "response_data" not in st.session_state:
    st.session_state.response_data = None

meal_type = st.selectbox("Select Meal Type", ["dinner", "breakfast", "entry", "snacks"])

input_method = st.radio("Choose input method:", ("Enter SRN Manually", "Scan QR Code"))

if input_method == "Enter SRN Manually":
    srn_input = st.text_input("Enter SRN:")
    if st.button("Submit"):
        if srn_input:
            st.session_state.qr_data = srn_input
            response = requests.post(f"{API_URL}/{meal_type}", json={"srn": st.session_state.qr_data})
            if response.status_code == 200:
                st.session_state.response_data = response.json()
                st.success("✅ Response received!")
            else:
                st.error("❌ Error sending data. Try again!")
                print(f"Error response: {response.status_code}, {response.text}")

elif input_method == "Scan QR Code":
    qr_data = qrcode_scanner()
    if qr_data:
        st.session_state.qr_data = qr_data
        st.success(f"Scanned QR Data: {st.session_state.qr_data}")
        if st.button("Submit"):
            response = requests.post(f"{API_URL}/{meal_type}", json={"srn": st.session_state.qr_data})
            if response.status_code == 200:
                st.session_state.response_data = response.json()
                st.success("✅ Response received!")
            else:
                st.error("❌ Error sending data. Try again!")
                print(f"Error response: {response.status_code}, {response.text}")

if st.session_state.response_data:
    st.write("Response Data:", st.session_state.response_data)

if st.button("Finish"):
    st.session_state.qr_data = None
    st.session_state.response_data = None
    st.success("Flow has been reset. You can start again.")
