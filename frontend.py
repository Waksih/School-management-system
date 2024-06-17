import streamlit as st
import requests
import pandas as pd


BASE_URL = 'http://localhost:5000'

st.title("School Management System")

#Sidebar for navigation
st.sidebar.title("Menu")
choice = st.sidebar.radio("Go to", ["Student Management", "Fee Management", "Expenditure Management", "Activity Management", "Student Activity Management", "Activity Participation Management", "Income Management"])

#Function to handle API responses
def handle_response(response):
    if response.status_code in [200, 201]:
        data = response.json()
        if data:  # Check if the list is not empty
            return data
        else:
            st.write("No records found.")
            return None
    else:
        st.error("Error fetching data.")
        return []

#Function for fetching records
def fetch_data(endpoint):
    response = requests.get(f"{BASE_URL}/{endpoint}")
    return handle_response(response)

#initialize session state for form visibility
if "show_form" not in st.session_state:
    st.session_state.show_form = False



# Student Management Section
if choice == "Student Management":
    st.header("Student Management")

    
    # Button to add a new student
    if st.button("Add Student"):
        st.session_state.show_form = True

    # Display the form if show_form is True
    if st.session_state.show_form:
        #Add student form
        st.write("Add a new student:")
        with st.form(key='student_form'):
                name = st.text_input("Student Name")
                class_name = st.text_input("Class Name")
                parent1_name = st.text_input("Parent 1 Name")
                parent1_phone = st.text_input("Parent 1 Phone")
                parent2_name = st.text_input("Parent 2 Name")
                parent2_phone = st.text_input("Parent 2 Phone")
                fee_payable = st.number_input("Fee Payable")
                fee_status = st.selectbox("Fee Status", ["Complete", "Incomplete"])
                submit_button = st.form_submit_button(label='Submit')
                
                if submit_button:
                # Form validation
                    if not all([name, class_name, parent1_name, parent1_phone, parent2_name, parent2_phone, fee_payable, fee_status]):
                        st.error("All fields are required.")
                    else:
                        # Check for duplicates
                        students = fetch_data('students')
                        duplicate = any(student for student in students if student['name'] == name and student['class_name'] == class_name)
                        if duplicate:
                            st.error("This student is already entered.")
                        else:
                            student_data = {
                                "name": name,
                                "class_name": class_name,
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
                                st.session_state.show_form = False
                            else:
                                st.error("Error adding student")
        if st.button("Cancel"):
            st.session_state.show_form = False
            st.experimental_rerun()

    #Automatically fetch and display students
    students = fetch_data('students')
    if students:
        #Convert list of student dictionaries to a Dataframe
        df = pd.DataFrame(students, columns=[
            'name', 'class_name', 'parent1_name', 'parent1_phone',
            'parent2_name', 'parent2_phone', 'fee_payable', 'fee_status'
        ])
        st.dataframe(df)

# Fee Management Section
if choice == "Fee Management":
    st.header("Fee Management")
    
    # Button to add a new fee record
    if st.button("Add Fee Record"):
        st.session_state.show_form = True

    if st.session_state.show_form:
        # Add fee record form
        st.write("Add a new Fee Record")
        with st.form(key='fee_form'):
            student_name = st.text_input("Student Name")
            total_fees = st.number_input("Total Fees")
            amount_paid = st.number_input("Amount Paid")
            balance = st.number_input("Balance")
            remarks = st.text_area("Remarks")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                # Form validation
                if not all([student_id, total_fees, amount_paid, balance]):
                    st.error("All fields except remarks are required.")
                else:
                    fee_data = {
                        "student_name": student_name,
                        "total_fees": total_fees,
                        "amount_paid": amount_paid,
                        "balance": balance,
                        "remarks": remarks
                    }
                    response = requests.post(f"{BASE_URL}/fees", json=fee_data)
                    if response.status_code == 201:
                        st.success("Fee record added successfully!")
                        st.session_state.show_form = False
                    else:
                        st.error("Error adding fee record")
        if st.button("Cancel"):
            st.session_state.show_form = False
            st.experimental_rerun()

    # Automatically fetch and display fee records
    fees = fetch_data('fees')
    if fees:
        # Convert list of fee dictionaries to a Dataframe
        df = pd.DataFrame(fees, columns=[
            'student_name', 'total_fees', 'amount_paid', 
            'balance', 'remarks'
        ])
        st.dataframe(df)


# Expenditure Management Section
if choice == "Expenditure Management":
    st.header("Expenditure Management")

    # Button to add a new expenditure
    if st.button("Add Expenditure"):
        st.session_state.show_form = True

    if st.session_state.show_form:
        # Add expenditure form
        st.write("Add new Expenditure")
        with st.form(key='expenditure_form'):
            date = st.date_input("Date")
            item = st.text_input("Item")
            category = st.text_input("Category")
            vendor = st.text_input("Vendor")
            amount = st.number_input("Amount")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                # Form validation
                if not all([date, item, category, vendor, amount]):
                    st.error("All fields are required.")
                else:
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
                        st.session_state.show_form = False
                    else:
                        st.error("Error adding expenditure")
        if st.button("Cancel"):
            st.session_state.show_form = False
            st.experimental_rerun()

    # Automatically fetch and display expenditures
    expenditures = fetch_data('expenditures')
    if expenditures:
        # Convert list of expenditure dictionaries to a Dataframe
        df = pd.DataFrame(expenditures, columns=[
            "date","item","category","vendor","amount"
        ])
        st.dataframe(df)


# Activity Management Section
if choice == "Activity Management":
    st.header("Activity Management")

    # Button to add a new activity
    if st.button("Add Activity"):
        st.session_state.show_form = True

    if st.session_state.show_form:
        # Add activity form
        st.write("Add new Activity")
        with st.form(key='activity_form'):
            activity_name = st.text_input("Activity Name")
            payment_frequency = st.selectbox("Payment Frequency", ["Daily","Weekly","Monthly","termly"])
            fee_amount = st.number_input("Fee Amount")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                # Form validation
                if not all([activity_name, payment_frequency, fee_amount]):
                    st.error("All fields are required.")
                else:
                    activity_data = {
                        "activity_name": activity_name,
                        "payment_frequency": payment_frequency,
                        "fee_amount": fee_amount
                    }
                    response = requests.post(f"{BASE_URL}/activities", json=activity_data)
                    if response.status_code == 201:
                        st.success("Activity added successfully!")
                        st.session_state.show_form = False
                    else:
                        st.error("Error adding activity")
        if st.button("Cancel"):
            st.session_state.show_form = False
            st.experimental_rerun()

    # Automatically fetch and display activities
    activities = fetch_data('activities')
    if activities:
        # Convert list of activity dictionaries to a Dataframe
        df = pd.DataFrame(activities, columns=[
            "activity_name", "fee_amount", "payment_frequency"
        ])
        st.dataframe(df)


# Student Activity Management Section
if choice == "Student Activity Management":
    st.header("Student Activity Management")

    # Button to add a new student activity
    if st.button("Add Student Activity"):
        st.session_state.show_form = True

    if st.session_state.show_form:
        # Add student activity form
        st.write("Add new Participation Record")
        with st.form(key='student_activity_form'):
            student_name = st.text_input("Student Name")
            activity_name = st.text_input("Activity Name")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                # Form validation
                if not all([student_id, activity_id]):
                    st.error("All fields are required.")
                else:
                    student_activity_data = {
                        "student_name": student_name,
                        "activity_name": activity_name
                    }
                    response = requests.post(f"{BASE_URL}/student_activities", json=student_activity_data)
                    if response.status_code == 201:
                        st.success("Student activity added successfully!")
                        st.session_state.show_form = False
                    else:
                        st.error("Error adding student activity")
        if st.button("Cancel"):
            st.session_state.show_form = False
            st.experimental_rerun()

    # Automatically fetch and display student activities
    student_activities = fetch_data('student_activities')
    if student_activities:
        # Convert list of expenditure dictionaries to a Dataframe
        df = pd.DataFrame(student_activities, columns=[
            "student_name", "activity_name"
        ])
        st.dataframe(df)


# Activity Participation Management Section
if choice == "Activity Participation Management":
    st.header("Activity Participation Management")
    
    #Button to add new activity participation record
    if st.button("Add Participation Record"):
        st.session_state.show_form = True

    if st.session_state.show_form:
    # Add participation record form
        with st.form(key='participation_form'):
            student_name = st.text_input("Student Name")
            activity_name = st.text_input("Activity Name")
            term = st.number_input("Term", min_value=1)
            frequency = st.selectbox("Frequency", ["Daily","Weekly","Monthly","termly"])
            status = st.text_input("Status")
            date_paid_for = st.date_input("Date Paid For")
            amount_paid = st.number_input("Amount Paid")
            balance = st.number_input("Balance")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                # Form validation
                if not all([student_id, activity_id, term, week_or_month, participation_value]):
                    st.error("All fields are required.")
                else:
                    participation_data = {
                        "student_name": student_name,
                        "activity_name": activity_name,
                        "term": term,
                        "frequency": frequency,
                        "status": status,
                        "date_paid_for": date_paid_for.strftime('%Y-%m-%d'),
                        "amount_paid": amount_paid,
                        "balance": balance
                    }
                    response = requests.post(f"{BASE_URL}/activity_participation", json=participation_data)
                    if response.status_code == 201:
                        st.success("Participation record added successfully!")
                        st.session_state.show_form = False
                    else:
                        st.error("Error adding participation record")
        if st.button("Cancel"):
            st.session_state.show_form = False
            st.experimental_rerun()

    # Automatically fetch and display participation records
    participations = fetch_data('activity_participation')
    if participations:
        # Convert list of participation dictionaries to a Dataframe
        df = pd.DataFrame(participations, columns=[
            'student_name', 'activity_name', 'term', 
            'frequency', 'status', 'date_paid_for', 
            'amount_paid', 'balance'
        ])
        st.dataframe(df)


# Income Management Section
if choice == "Income Management":
    st.header("Income Management")
    
    # Button to add a new income record
    if st.button("Add Income Record"):
        st.session_state.show_form = True

    if st.session_state.show_form:
        # Add income record form
        st.write("Add new income record")
        with st.form(key='income_form'):
            student_name = st.text_input("Student Name")
            source = st.text_input("Source")
            amount = st.number_input("Amount")
            date = st.date_input("Date")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                # Form validation
                if not all([source, amount, date]):
                    st.error("All fields are required.")
                else:
                    income_data = {
                        "student_name": student_name,
                        "source": source,
                        "amount": amount,
                        "date": str(date)
                    }
                    response = requests.post(f"{BASE_URL}/income", json=income_data)
                    if response.status_code == 201:
                        st.success("Income record added successfully!")
                        st.session_state.show_form = False
                    else:
                        st.error("Error adding income record")
        if st.button("Cancel"):
            st.session_state.show_form = False
            st.experimental_rerun()

    # Automatically fetch and display income records
    income_records = fetch_data('income')
    if income_records:
        # Convert list of income dictionaries to a Dataframe
        df = pd.DataFrame(income_records, columns=[
            "student_name", "source", "amount", "date"
        ])
        st.dataframe(df)