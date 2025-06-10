import streamlit as st
import requests

st.set_page_config(page_title="School Loan System")
st.title("🏫 School Loan Calculator")

savings = st.number_input("Enter your total savings (UGX)", min_value=0, step=100)

if st.button("Calculate Loan"):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/calculate-loan",
            json={"savings": savings}
        )
        if response.status_code == 200:
            result = response.json()
            st.success(f"💰 You qualify for a loan of UGX {result['loan_amount']:,}")
        else:
            st.error("⚠️ Server error. Please try again.")
    except Exception as e:
        st.error(f"⚠️ Could not connect to the backend. {e}")
