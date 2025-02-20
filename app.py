import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Page Configuration
st.set_page_config(
    page_title="Women's Health",
    page_icon="🎀",
    layout="wide",
)

# Google Sheets Authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# Open Google Sheet
sheet = client.open("users_data").sheet1  # Replace with your sheet name

# Function to save new user data
def save_user(name, email, password):
    emails = sheet.col_values(2)  # Get all emails (column 2)
    
    if email in emails:
        st.warning("Email already registered. Please log in.")
    else:
        sheet.append_row([name, email, password])
        st.success("User registered successfully! Please log in.")

# Function to verify user
def verify_user(email, password):
    users = sheet.get_all_records()
    return any(user.get("Email") == email and user.get("Password") == password for user in users)

# Login/Signup Page
st.title("Login/Signup")
action = st.selectbox("Choose Action", ["Login", "Signup"])

name = st.text_input("Name") if action == "Signup" else None
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if action == "Signup":
    if st.button("Sign Up"):
        if name and email and password:
            save_user(name, email, password)
        else:
            st.error("Please fill all fields.")

elif action == "Login":
    if st.button("Log In"):
        if verify_user(email, password):
            st.success("Login successful! Redirecting...")
        else:
            st.error("Invalid email or password.")
