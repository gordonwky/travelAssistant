import streamlit as st
import requests

API_BASE = "http://localhost:8000"  # replace with your backend URL

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "token" not in st.session_state:
    st.session_state.token = None

st.title("🔐 Auth with Backend")

menu = st.sidebar.radio("Menu", ["Sign Up", "Login", "Dashboard"])

# --- SIGN UP ---
if menu == "Sign Up":
    st.subheader("Create Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        try:
            resp = requests.post(f"{API_BASE}/api/signup", data={
                "username": new_user,
                "password": new_pass
            })
            if resp.status_code == 201:
                st.success("Account created! You can now log in.")
            else:
                st.error(resp.json().get("detail", "Signup failed"))
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")

# --- LOGIN ---
elif menu == "Login":
    st.subheader("Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            resp = requests.post(f"{API_BASE}/api/login", data={
                "username": user,
                "password": pwd
            })
            if resp.status_code == 200:
                data = resp.json()
                st.session_state.logged_in = True
                st.session_state.username = user
                st.session_state.token = data.get("access_token")  # e.g. JWT
                st.success(f"Welcome {user}!")
            else:
                st.error(resp.json().get("detail", "Login failed"))
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")

# --- DASHBOARD ---
elif menu == "Dashboard":
    if st.session_state.logged_in:
        st.success(f"Hello, {st.session_state.username}!")
        st.write("Your token:", st.session_state.token)

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.token = None
    else:
        st.warning("Please login first.")
