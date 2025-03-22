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

            st.write("Response Status:", response.status_code)
            st.write("Response Text:", response.text)

            if response.status_code == 200:
                st.session_state.response_data = response.json()
                st.success("✅ Response received!")
            else:
                st.error(f"❌ Error sending data. Try again! (Status: {response.status_code})")

elif input_method == "Scan QR Code":
    qr_data = qrcode_scanner()
    if qr_data:
        st.session_state.qr_data = qr_data
        st.success(f"Scanned QR Data: {st.session_state.qr_data}")

        response = requests.post(f"{API_URL}/{meal_type}", json={"srn": st.session_state.qr_data})

        st.write("Response Status:", response.status_code)
        st.write("Response Text:", response.text)

        if response.status_code == 200:
            st.session_state.response_data = response.json()
            st.success("✅ Response received!")
        else:
            st.error(f"❌ Error sending data. Try again! (Status: {response.status_code})")

if st.session_state.response_data:
    st.write("Server Response:")
    st.json(st.session_state.response_data)  

if st.button("Finish"):
    st.session_state.clear()
    st.rerun()
    

