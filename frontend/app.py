import streamlit as st
import requests
from streamlit_qrcode_scanner import qrcode_scanner

API_URL = "https://heal-o-code.vercel.app"

st.title("QR Scanner for Meals Check-in")

if "meal_type" not in st.session_state:
    st.session_state.meal_type = None
if "input_method" not in st.session_state:
    st.session_state.input_method = None
if "qr_data" not in st.session_state:
    st.session_state.qr_data = None
if "response_data" not in st.session_state:
    st.session_state.response_data = None

st.session_state.meal_type = st.selectbox("Select Meal Type", ["dinner", "breakfast", "entry", "snacks"], index=0)

st.session_state.input_method = st.radio("Choose input method:", ("Enter SRN Manually", "Scan QR Code"))

if st.session_state.input_method == "Enter SRN Manually":
    srn_input = st.text_input("Enter SRN:")
    if st.button("Submit"):
        if srn_input:
            st.session_state.qr_data = srn_input  
            response = requests.post(f"{API_URL}/{st.session_state.meal_type}", json={"srn": srn_input})
            if response.status_code == 200:
                st.session_state.response_data = response.json()
                st.success("✅ Response received!")
            else:
                st.error("❌ Error sending data. Try again!")
                print(f"Error response: {response.status_code}, {response.text}")

elif st.session_state.input_method == "Scan QR Code":
    qr_data = qrcode_scanner()  

    if qr_data:  
        st.session_state.qr_data = qr_data
        st.success(f"✅ Scanned QR Data: {qr_data["srn"]}")

        if st.button("Submit"):
            response = requests.post(f"{API_URL}/{st.session_state.meal_type}", json={"srn": qr_data["srn"]})
            if response.status_code == 200:
                st.session_state.response_data = response.json()
                st.success("✅ Response received!")
            else:
                st.error("❌ Error sending data. Try again!")
                print(f"Error response: {response.status_code}, {response.text}")

if st.session_state.response_data:
    st.write("🔹 **SRN:**", st.session_state.response_data["srn"])
    st.write("🔹 **Response Data:**", st.session_state.response_data["status"])

if st.button("View Database"):
    response = requests.get(f"{API_URL}/database")
    if response.status_code == 200:
        database_data = response.json()
        st.write("🔹 **Database Data:**")
        if "data" in database_data:
            st.table(database_data["data"])
        else:
            st.error("❌ No data found in the response.")
    else:
        st.error("❌ Error fetching database. Try again!")
        print(f"Error response: {response.status_code}, {response.text}")

if st.button("Finish"):
    st.session_state.clear()  
    st.rerun()  
