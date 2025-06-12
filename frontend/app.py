import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="School Loan System")
st.title("🏫 School Loan Calculator")

menu = st.sidebar.selectbox("Menu", ["Save Monthly Amount", "Request Loan"])

if menu == "Save Monthly Amount":
    st.subheader("🏦 Submit Your Monthly Saving")
    user_id = st.text_input("Enter your User ID")
    amount = st.number_input("Enter Monthly Saving Amount", min_value=0.0, step=100.0)

    if st.button("Save"):
        if user_id and amount > 0:
            response = requests.post(f"{API_URL}/save", json={
                "user_id": user_id,
                "monthly_saving": amount
            })
            if response.status_code == 200:
                st.success("Savings recorded successfully!")
            else:
                st.error(response.json().get("detail"))
        else:
            st.warning("Please enter valid details.")

elif menu == "Request Loan":
    st.subheader("💰 Check Loan Eligibility")
    user_id = st.text_input("Enter your User ID")

    if st.button("Check Loan"):
        if user_id:
            response = requests.post(f"{API_URL}/loan", json={"user_id": user_id})
            if response.status_code == 200:
                loan = response.json()["loan_eligible_amount"]
                st.success(f"You're eligible for a loan of UGX {loan:,.0f}")
            else:
                st.error(response.json().get("detail"))
        else:
            st.warning("Please enter your User ID.")