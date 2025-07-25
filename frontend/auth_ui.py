import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv("API_URL")

def show_auth_sidebar():
    st.sidebar.title("Authentication")

    if st.session_state.get("logged_out"):
        st.success("You have been logged out.")
        del st.session_state["logged_out"]

    if "token" not in st.session_state:
        option = st.sidebar.radio("Choose:", ["Login", "Register"])
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if option == "Login" and st.sidebar.button("Login"):
            login(username, password)
        elif option == "Register" and st.sidebar.button("Register"):
            register(username, password)
    else:
        st.sidebar.success(f"Logged in as {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.session_state["logged_out"] = True
            st.rerun()

def register(username, password):
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "username": username.strip(),
            "password": password
        }
        res = requests.post(
            f"{API_URL}/register",
            json=payload, headers=headers
        )

        if res.status_code == 200:
            st.success("Registration successful! You can now log in.")

        else:
            try:
                error = res.json().get("detail", "Registration failed")
            except:
                error = res.text
            st.error(f"{error}")
    except Exception as e:
        st.error(f"Registration error: {e}")

def login(username, password):
    try:
        res = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if res.status_code == 200:
            st.session_state["token"] = res.json()["access_token"]
            st.session_state["username"] = username
            st.success("Logged in successfully")
            st.rerun()
        else:
            st.error("Invalid credentials")
    except Exception as e:
        st.error(f"Login failed: {e}")

def logout():
    st.session_state.clear()
    st.session_state["logged_out"] = True
    st.success("You have been logged out.")
    st.rerun()


