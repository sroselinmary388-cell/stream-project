import streamlit as st
import requests

# Backend API URL
BASE_URL = "http://localhost:8000"  # Adjust if your FastAPI runs on a different host/port

st.title("Student Record Management")

# Operation selection
operation = st.selectbox("Select Operation", ["Insert", "Update", "Delete"])

# Common input fields
s_no = st.text_input("Serial No (s_no)")

# Show/hide fields based on operation
name = department = age = cutoff = None

if operation == "Insert":
    name = st.text_input("Name")
    department = st.text_input("Department")
    age = st.number_input("Age", min_value=0, step=1)
    cutoff = st.number_input("Cutoff", min_value=0.0, step=0.1)

elif operation == "Update":
    name = st.text_input("New Name")

# Submit button
if st.button(f"{operation} Record"):
    # Prepare the request payload
    payload = {"s_no": s_no}

    if operation == "Insert":
        payload.update({
            "name": name,
            "department": department,
            "age": age,
            "cutoff": cutoff
        })
        response = requests.post(f"{BASE_URL}/insert/", json=payload)

    elif operation == "Update":
        payload["name"] = name
        response = requests.post(f"{BASE_URL}/update/", json=payload)

    elif operation == "Delete":
        response = requests.post(f"{BASE_URL}/delete/", json=payload)

    # Handle response
    if response.status_code == 200:
        data = response.json()
        st.success(data["message"])
        st.subheader("Updated Student Table")
        students = data["all_students"]
        if students:
            import pandas as pd

            df = pd.DataFrame(students, columns=["s_no", "name", "department", "age", "cutoff"])
            st.dataframe(df)
        else:
            st.info("No records found.")
    else:
        st.error("Operation failed! Check inputs and backend.")
