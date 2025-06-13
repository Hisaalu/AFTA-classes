import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="School Loan System")
st.title("🏫 School Loan Calculator")

menu = st.sidebar.radio("Select Option", ["Register Savings Plan", "Check Loan Eligibility"])

if menu == "Register Savings Plan":
    st.subheader("📅 Monthly Saving Setup")
    user_id = st.text_input("Enter your User ID")
    monthly_saving = st.number_input("Monthly Saving (UGX)", min_value=0.0, step=100.0)

    if st.button("Register Plan"):
        if user_id and monthly_saving > 0:
            res = requests.post(f"{API_URL}/save", json={
                "user_id": user_id,
                "monthly_saving": monthly_saving
            })
            if res.status_code == 200:
                st.success("Your Monthly Saving Plan has been Saved")
                st.info(f"Saving started on: {res.json()['start_date']}")
            else:
                st.error(res.json().get("detail"))
        else:
            st.warning("Please fill in all feilds.")

elif menu == "Check Loan Eligibility":
    st.subheader("💳 Loan Estimator")
    user_id = st.text_input("Enter your User ID")

    if st.button("Calculate Loan"):
        if user_id:
            res = requests.post(f"{API_URL}/loan", json={"user_id": user_id})
            if res.status_code == 200:
                data = res.json()
                st.success(f"Start Date: {data['start_date']}")
                st.info(f"Months Saved: {data['months_saved']}")
                st.success(f"Total Saved: UGX {data['total_saved']:,.0f}")
                st.success(f"Loan Eligible: UGX {data['loan_eligible_amount']:,.0f}")
            else:
                st.error(res.json().get("detail"))
        else:
            st.warning("Please enter your User ID.")