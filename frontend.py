import streamlit as st
import requests
import pandas as pd

# Apply custom CSS
st.markdown(
    """
    <style>
    body {
    display: flex;
    margin: 0;
    padding: 0;
    background-color: #121212; /* Ensure the background color matches */
    }

    .sidebar.st-emotion-cache-1itdyc2 {
        width: 200px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        position: fixed;
        height: 100%;
        background-color: #1f1f1f; /* Sidebar background color to match the theme */
    }

    .main-content-container {
        flex-grow: 1;
        margin-left: 220px; /* Adjust according to sidebar width + padding */
        padding: 20px 20px 20px 20px;
        box-sizing: border-box;
        max-width: calc(100% - 220px); /* Ensure content doesn't overflow */
        margin-top: 0; /* Ensure content starts at the top */
        padding-top: 0; /* Remove any padding at the top */
    }

    /* Existing styles */
    .st-emotion-cache-1aege4m {
        width: 100% !important; /* Take full width of the container */
        max-width: 100%; /* Ensure it doesn't exceed the container */
    }

    .st-emotion-cache-ul70r3 {
        max-width: 100%; /* Ensure inner content also respects the container width */
    }

    /* Optimize text spacing within the sidebar */
    .st-ag.st-ce.st-cf.st-cg.st-as.st-ch.st-ci {
        padding: 0 !important;
    }

    /* Label adjustments */
    .st-aj.st-ag.st-cj.st-as.st-aw.st-ck.st-ax.st-b1.st-cl.st-cm.st-cn.st-co.st-cp.st-cq {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Div adjustments */
    .st-b0.st-dd.st-cr.st-cs.st-ct.st-cu.st-cv.st-ag.st-cw.st-bv.st-cx.st-av.st-cy.st-cz.st-bi.st-d0.st-d1.st-d2.st-bg.st-d3 {
        padding: 0 !important;
    }

    /* Paragraph adjustments */
    .st-d0.st-da.st-c1.st-bp.st-db.st-br.st-bs.st-bt.st-bu.st-af.st-dc p {
        margin: 0 !important;
        padding: 5px 10px !important;
    }

    /* Change font size of main tabs */
    div[data-testid="stHorizontalBlock"] > div > div {
        font-size: 2rem;
    }

    /* Change font size of sub-tabs */
    div[data-testid="stHorizontalBlock"] > div > div > div > div {
        font-size: 1.2rem;
    }

    /* Title customization */
    .main-title {
        text-align: center;
        font-size: 4rem;
        color: #ff6347;
        font-weight: bold;
        
    }

    /* Subtitle customization */
    .sub-title {
        text-align: center;
        font-size: 2.5rem;
        color: #ffffff;
    }

    /* Section headers customization */
    .section-header {
        text-align: center;
        font-size: 2rem;
        color: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True
)


BASE_URL = 'http://localhost:5000'


# Title at the top
st.markdown("<div class='main-title'>The Spark Playhouse</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>School Management System</div>", unsafe_allow_html=True)


#Sidebar for navigation
st.sidebar.title("Menu")
choice = st.sidebar.radio("Go to", ["Students", "Fees", "Expenditure", "Activities", "Student Activity", "Activity Participation", "Income"])

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
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch {endpoint} data")
            return []
    except Exception as e:
        st.error(f"Error fetching {endpoint} data: {e}")
        return []


# Student Management Section
if choice == "Students":
    st.markdown("<div class='section-header'>Student Management</div>", unsafe_allow_html=True)

    #create tabs
    tab1, tab2, tab3 = st.tabs(["Students", "Daycare", "Analytics"])

    with tab1:
        student_tab1, student_tab2 = st.tabs(["View Students", "Add Student"])

        #Students tab 
        with student_tab1:
            #Fetch student data
            students = fetch_data('students')
            if students:
            #Convert list of student dictionaries to a Dataframe
                df = pd.DataFrame(students, columns=[
                'name', 'class_name', 'parent1_name', 'parent1_phone',
                'parent2_name', 'parent2_phone', 'fee_payable', 'fee_status'
                ])
                st.dataframe(df)
            else:
                st.write("No students to display.")

        with student_tab2:
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
                            if students is None:
                                students = []
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
                                    st.rerun()
                                else:
                                    error_message = response.json().get('error', 'Unknown error')
                                    st.error(f"Error adding student: {error_message}")
                                    st.rerun()

    with tab2:

        daycare_tab1, daycare_tab2 = st.tabs(["View Children", "Add child"])

        with daycare_tab1:

            #Automatically fetch and display students
            daycare = fetch_data('daycare')
            if daycare:
                #Convert list of daycare dictionaries to a Dataframe
                df = pd.DataFrame(daycare, columns=[
                    'name', 'parent_1_name', 'parent_1_phone', 'parent_2_name', 'parent_2_phone',
                    'payment_mode', 'option', 'fee_payable', 'fee_paid',
                    'balance', 'status'
                ])
                st.dataframe(df)
            else:
                st.write("No children to display.") 

        with daycare_tab2:
            #Add daycare form
            st.write("Add a new child:")
            with st.form(key='daycare_form'):
                name = st.text_input("Child's Name")
                parent_1_name = st.text_input("Parent 1 Name")
                parent_1_phone = st.text_input("Parent 1 Phone")
                parent_2_name = st.text_input("Parent 2 Name")
                parent_2_phone = st.text_input("Parent 2 Phone")
                payment_mode = st.selectbox("Payment mode", ["Daily", "Weekly", "Monthly"])
                option = st.selectbox("Option", ["Home meals", "School meals"])
                fee_payable = st.number_input("Fee Payable")
                fee_paid = st.number_input("Fee Paid")
                balance = st.number_input("Balance")
                status = st.selectbox("Status", ["Complete", "Incomplete", "Paid", "Unpaid"])
                submit_button = st.form_submit_button(label='Submit')
                
                if submit_button:
                # Form validation
                    if not all([name, parent_1_name, parent_1_phone, payment_mode, option, fee_payable, fee_paid, balance, status]):
                        st.error("All fields are required.")
                    else:
                        # Check for duplicates
                        daycare = fetch_data('daycare')
                        if daycare is None:
                            daycare = []
                        duplicate = any(daycare for daycare in daycare if daycare['name'] == name )
                        if duplicate:
                            st.error("This child is already entered.")
                        else:
                            daycare_data = {
                                "name": name,                                
                                "parent_1_name": parent_1_name,
                                "parent_1_phone": parent_1_phone,
                                "parent_2_name": parent_2_name,
                                "parent_2_phone": parent_2_phone,
                                "payment_mode" : payment_mode,
                                "option" : option,                        
                                "fee_payable": fee_payable,
                                "fee_paid": fee_paid,
                                "balance" : balance,
                                "status" : status
                            }
                            response = requests.post(f"{BASE_URL}/daycare", json=daycare_data)
                            if response.status_code == 201:
                                st.success("Child added successfully!")
                                st.session_state.show_form = False
                                st.rerun()
                            else:
                                error_message = response.json().get('error', 'Unknown error')
                                st.error(f"Error adding child: {error_message}")
                                st.rerun()
                                                                       
            
# Fee Management Section
if choice == "Fees":
    st.markdown("<div class='section-header'>Fee Management</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Records", "Add Record", "Analytics"])

    with tab1:
        # Automatically fetch and display fee records
        fees = fetch_data('fees')
        if fees:
            # Convert list of fee dictionaries to a Dataframe
            df = pd.DataFrame(fees, columns=[
                'student_name', 'total_fees', 'amount_paid', 
                'balance', 'remarks'
            ])
            st.dataframe(df)
        else:
            st.write("No Fee records to display.")

    with tab2:
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
                if not all([student_name, total_fees is not None,amount_paid is not None, balance is not None]):
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
                        st.rerun()
                    else:
                        st.error("Error adding fee record")
                        st.rerun()


# Expenditure Management Section
if choice == "Expenditure":
    st.markdown("<div class='section-header'>Expenditure Management</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Expenses", "Add Expenses", "Analysis"])

    with tab1:
        # Automatically fetch and display expenditures
        expenditures = fetch_data('expenditures')
        if expenditures:
            # Convert list of expenditure dictionaries to a Dataframe
            df = pd.DataFrame(expenditures, columns=[
                "date","item","category","vendor","amount"
            ])
            st.dataframe(df)
        else:
            st.write("No expenditures to display.")

    with tab2: 
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
                if not all([date, item, category, vendor, amount is not None]):
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
                        st.rerun()
                    else:
                        st.error("Error adding expenditure")
                        st.rerun()

    
# Activity Management Section
if choice == "Activities":
    st.markdown("<div class='section-header'>Activity Management</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Activities", "Add activity"])
    
    with tab1:
        # Automatically fetch and display activities
        activities = fetch_data('activities')
        if activities:
            # Convert list of activity dictionaries to a Dataframe
            df = pd.DataFrame(activities, columns=[
                "activity_name", "fee_amount", "payment_frequency"
            ])
            st.dataframe(df)
        else:
            st.write("No activities to display.")
    
    with tab2:
        st.write("Add new Activity")
        with st.form(key='activity_form'):
            activity_name = st.text_input("Activity Name")
            payment_frequency = st.selectbox("Payment Frequency", ["Daily","Weekly","Monthly","termly"])
            fee_amount = st.number_input("Fee Amount")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                # Form validation
                if not all([activity_name, payment_frequency, fee_amount is not None]):
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
                        st.rerun()
                    else:
                        st.error("Error adding activity")
                        st.rerun()


# Student Activity Management Section
if choice == "Student Activity":
    st.markdown("<div class='section-header'>Student Activity Management</div>", unsafe_allow_html=True)

    tab1,tab2, tab3 = st.tabs(["Student Activities","Add Std Activity","Analysis"])

    with tab1:
        # Automatically fetch and display student activities
        student_activities = fetch_data('student_activities')
        if student_activities:
            # Convert list of expenditure dictionaries to a Dataframe
            df = pd.DataFrame(student_activities, columns=[
                "student_name", "activity_name"
            ])
            st.dataframe(df)
        else:
            st.write("No students activities to display.")

    with tab2:
        # Add student activity form
        st.write("Add new Student Activity")
        with st.form(key='student_activity_form'):
            student_name = st.text_input("Student Name")
            activity_name = st.text_input("Activity Name")
            submit_button = st.form_submit_button(label='Submit')
            
            if submit_button:
                # Form validation
                if not all([student_name, activity_name]):
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
                        st.rerun()
                    else:
                        st.error("Error adding student activity")
                        st.rerun()


# Activity Participation Management Section
if choice == "Activity Participation":
    st.markdown("<div class='section-header'>Activity Participation Management</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Participation records","Add record","Analysis"])

    with tab1:
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
        else:
            st.write("No participations to display.")
    
    with tab2:
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
                if not all([student_name, activity_name, term, frequency, status, date_paid_for,amount_paid is not None, balance is not None]):
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
                        st.rerun()
                    else:
                        st.error("Error adding participation record")
                        st.rerun()


# Income Management Section
if choice == "Income":
    st.markdown("<div class='section-header'>Income Management</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Income records","Add income","Analysis"])

    with tab1:
        # Automatically fetch and display income records
        income_records = fetch_data('income')
        if income_records:
            # Convert list of income dictionaries to a Dataframe
            df = pd.DataFrame(income_records, columns=[
                "student_name", "source", "amount", "date"
            ])
            st.dataframe(df)
        else:
            st.write("No income records to display.")
    
    with tab2:
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
                if not all([student_name, source, amount is not None, date]):
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
                        st.rerun()
                    else:
                        st.error("Error adding income record")
                        st.rerun()
       