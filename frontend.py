import streamlit as st
import requests

BASE_URL = 'http://localhost:5000'

st.title("School Management System")

menu = ["Student Management", "Fee Management", "Expenditure Management", "Activity Management", "Student Activity Management", "Activity Participation Management", "Income Management"]
choice = st.sidebar.selectbox("Select a section", menu)


# Student Management Section
if choice == "Student Management":
    st.header("Student Management")
    if st.button("Get Students"):
        response = requests.get(f"{BASE_URL}/students")
        students = response.json()
        for student in students:
            st.write(student)
    
    if st.button("Add Student"):
        with st.form(key='student_form'):
            name = st.text_input("Student Name")
            class_ = st.text_input("Class")
            parent1_name = st.text_input("Parent 1 Name")
            parent1_phone = st.text_input("Parent 1 Phone")
            parent2_name = st.text_input("Parent 2 Name")
            parent2_phone = st.text_input("Parent 2 Phone")
            fee_payable = st.number_input("Fee Payable")
            fee_status = st.selectbox("Fee Status", ["Complete", "Incomplete"])
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                student_data = {
                    "name": name,
                    "class": class_,
                    "parent1_name": parent1_name,
                    "parent1_phone": parent1_phone,
                    "parent2_name": parent2_name,
                    "parent2_phone": parent2_phone,
                    "fee_payable": fee_payable,
                    "fee_status": fee_status
                }
                response = requests.post(f"{BASE_URL}/students", json=student_data)
                if response.status_code == 201:
                    st.success("Student added successfully!")
                else:
                    st.error("Error adding student")

# Fee Management Section
if choice == "Fee Management":
    st.header("Fee Management")
    if st.button("Get Fees"):
        response = requests.get(f"{BASE_URL}/fees")
        fees = response.json()
        for fee in fees:
            st.write(fee)
    
    if st.button("Add Fee Record"):
        with st.form(key='fee_form'):
            student_id = st.number_input("Student ID", min_value=1)
            total_fees = st.number_input("Total Fees")
            amount_paid = st.number_input("Amount Paid")
            balance = st.number_input("Balance")
            remarks = st.text_area("Remarks")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                fee_data = {
                    "student_id": student_id,
                    "total_fees": total_fees,
                    "amount_paid": amount_paid,
                    "balance": balance,
                    "remarks": remarks
                }
                response = requests.post(f"{BASE_URL}/fees", json=fee_data)
                if response.status_code == 201:
                    st.success("Fee record added successfully!")
                else:
                    st.error("Error adding fee record")

# Expenditure Management Section
if choice == "Expenditure Management":
    st.header("Expenditure Management")
    if st.button("Get Expenditures"):
        response = requests.get(f"{BASE_URL}/expenditures")
        expenditures = response.json()
        for expenditure in expenditures:
            st.write(expenditure)
    
    if st.button("Add Expenditure"):
        with st.form(key='expenditure_form'):
            date = st.date_input("Date")
            item = st.text_input("Item")
            category = st.text_input("Category")
            vendor = st.text_input("Vendor")
            amount = st.number_input("Amount")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                expenditure_data = {
                    "date": str(date),
                    "item": item,
                    "category": category,
                    "vendor": vendor,
                    "amount": amount
                }
                response = requests.post(f"{BASE_URL}/expenditures", json=expenditure_data)
                if response.status_code == 201:
                    st.success("Expenditure added successfully!")
                else:
                    st.error("Error adding expenditure")

# Activity Management Section
if choice == "Activity Management":
    st.header("Activity Management")
    if st.button("Get Activities"):
        response = requests.get(f"{BASE_URL}/activities")
        activities = response.json()
        for activity in activities:
            st.write(activity)
    
    if st.button("Add Activity"):
        with st.form(key='activity_form'):
            activity_name = st.text_input("Activity Name")
            payment_frequency = st.text_input("Payment Frequency")
            fee_amount = st.number_input("Fee Amount")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                activity_data = {
                    "activity_name": activity_name,
                    "payment_frequency": payment_frequency,
                    "fee_amount": fee_amount
                }
                response = requests.post(f"{BASE_URL}/activities", json=activity_data)
                if response.status_code == 201:
                    st.success("Activity added successfully!")
                else:
                    st.error("Error adding activity")

# Student Activity Management Section
if choice == "Student Activity Management":
    st.header("Student Activity Management")
    if st.button("Get Student Activities"):
        response = requests.get(f"{BASE_URL}/student_activities")
        student_activities = response.json()
        for student_activity in student_activities:
            st.write(student_activity)
    
    if st.button("Add Student Activity"):
        with st.form(key='student_activity_form'):
            student_id = st.number_input("Student ID", min_value=1)
            activity_id = st.number_input("Activity ID", min_value=1)
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                student_activity_data = {
                    "student_id": student_id,
                    "activity_id": activity_id
                }
                response = requests.post(f"{BASE_URL}/student_activities", json=student_activity_data)
                if response.status_code == 201:
                    st.success("Student Activity added successfully!")
                else:
                    st.error("Error adding student activity")

# Activity Participation Management Section
if choice == "Activity Participation Management":
    st.header("Activity Participation Management")
    if st.button("Get Activity Participations"):
        response = requests.get(f"{BASE_URL}/activity_participation")
        participations = response.json()
        for participation in participations:
            st.write(participation)
    
    if st.button("Add Participation Record"):
        with st.form(key='participation_form'):
            student_id = st.number_input("Student ID", min_value=1)
            activity_id = st.number_input("Activity ID", min_value=1)
            term = st.number_input("Term", min_value=1)
            week_or_month = st.text_input("Week or Month")
            participation_value = st.number_input("Participation Value", min_value=1)
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                participation_data = {
                    "student_id": student_id,
                    "activity_id": activity_id,
                    "term": term,
                    "week_or_month": week_or_month,
                    "participation_value": participation_value
                }
                response = requests.post(f"{BASE_URL}/activity_participation", json=participation_data)
                if response.status_code == 201:
                    st.success("Participation record added successfully!")
                else:
                    st.error("Error adding participation record")