import streamlit as st
import pandas as pd
import requests
import os
from io import StringIO

API_URL = "https://school-loan-backend.onrender.com"
#API_URL = "http://127.0.0.1:8000"


#BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#CSV_FILE = os.path.join(BASE_DIR, "../shared_data/savings.csv")

st.set_page_config(page_title="School Loan System")
st.title("🏫 School Loan Calculator")

menu = st.sidebar.radio("Select Option", ["Register Savings Plan", "Check Loan Eligibility", "Download CSV"])

if menu == "Register Savings Plan":
    st.subheader("📅 Enter Monthly Savings")
    user_id = st.text_input("User ID").strip().lower()
    monthly = st.number_input("Monthly Saving (UGX)", step=1000.0)

    if st.button("Save"):
            try: 
                res = requests.post(f"{API_URL}/save", json={
                    "user_id": user_id,
                    "monthly_saving": monthly
                })
                if res.status_code == 200:
                    st.success(res.json()["message"])
                else:
                    try:
                        st.error(res.json().get("detail", "Error saving data."))  # CHANGED
                    except:
                        st.error("Server error.")
            except requests.exceptions.RequestException as e: 
                st.error(f"Connection error: {e}")

elif menu == "Check Loan Eligibility":
    st.subheader("💳 Check Loan Eligibility")
    user_id = st.text_input("User ID").strip().lower()

    if st.button("Get Loan Info"):
        if user_id:
            try: 
                res = requests.post(f"{API_URL}/loan", json={"user_id": user_id})
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"Months Saved: {data['months_saved']}")
                    st.info(f"Total Saved: UGX {data['total_saved']:,.0f}")
                    st.success(f"Loan Eligible: UGX {data['loan_eligible_amount']:,.0f}")
                else:
                    try:
                        st.error(res.json().get("detail", "Error checking loan."))  # CHANGED
                    except Exception:
                        st.error(f"Server error: {res.status_code}")
            except requests.exceptions.RequestException as e: 
                st.error(f"Connection error: {e}")

elif menu == "Download CSV":
    st.subheader("📁 Current Savings Data")
    try: 
        res = requests.get(f"{API_URL}/csv")
        if res.status_code == 200:
            df = pd.read_csv(StringIO(res.text)) 
            st.dataframe(df)

            st.download_button("📤 Download CSV", data=res.content, file_name="savings.csv", mime='text/csv')  # ADDED
        else:
            st.warning("Unable to fetch CSV from backend.")
    except Exception as e:
        st.error(f"Error fetching CSV: {e}") 

