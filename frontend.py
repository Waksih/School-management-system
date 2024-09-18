import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(layout="wide")

# Apply custom CSS
st.markdown(
    """
    <style>
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.2rem;
    }

    .sidebar.st-emotion-cache-1itdyc2 {
        width: 200px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        position: fixed;
        height: 100%;
        background-color: #1f1f1f; /* Sidebar background color to match the theme */
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

    /* Title customization */
    .main-title {
        text-align: center;
        font-size: 5rem;
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
    unsafe_allow_html=True,
)


BASE_URL = "http://localhost:5000"


# Title at the top
st.markdown("<div class='main-title'>The Spark Playhouse</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>School Management System</div>", unsafe_allow_html=True
)


# Sidebar for navigation
st.sidebar.title("Menu")
choice = st.sidebar.radio(
    "Go to",
    [
        "Students",
        "Fees",
        "Expenditure",
        "Activities",
        "Student Activity",
        "Activity Participation",
        "Income",
    ],
)


# Function to handle API responses
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


# Function for fetching records
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
    st.markdown(
        "<div class='section-header'>Student Management</div>", unsafe_allow_html=True
    )

    # create tabs
    tab1, tab2, tab3 = st.tabs(["Students", "Daycare", "Analytics"])

    with tab1:
        student_tab1, student_tab2 = st.tabs(["View Students", "Add Student"])

        # Students tab
        with student_tab1:
            # Fetch student data
            students = fetch_data("students")
            if students:
                # Convert list of student dictionaries to a Dataframe
                df = pd.DataFrame(
                    students,
                    columns=[
                        "name",
                        "class_name",
                        "parent1_name",
                        "parent1_phone",
                        "parent2_name",
                        "parent2_phone",
                        "fee_payable",
                        "fee_status",
                    ],
                )
                st.dataframe(df, use_container_width=True)
            else:
                st.write("No students to display.")

        with student_tab2:
            st.write("Add a new student:")
            with st.form(key="student_form"):
                name = st.text_input("Student Name")
                class_name = st.text_input("Class Name")
                parent1_name = st.text_input("Parent 1 Name")
                parent1_phone = st.text_input("Parent 1 Phone")
                parent2_name = st.text_input("Parent 2 Name")
                parent2_phone = st.text_input("Parent 2 Phone")
                fee_payable = st.number_input("Fee Payable")
                fee_status = st.selectbox("Fee Status", ["Complete", "Incomplete"])
                submit_button = st.form_submit_button(label="Submit")

                if submit_button:
                    # Form validation
                    if not all(
                        [
                            name,
                            class_name,
                            parent1_name,
                            parent1_phone,
                            parent2_name,
                            parent2_phone,
                            fee_payable,
                            fee_status,
                        ]
                    ):
                        st.error("All fields are required.")
                    else:
                        # Check for duplicates
                        students = fetch_data("students")
                        if students is None:
                            students = []
                        duplicate = any(
                            student
                            for student in students
                            if student["name"] == name
                            and student["class_name"] == class_name
                        )
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
                                "fee_status": fee_status,
                            }
                            response = requests.post(
                                f"{BASE_URL}/students", json=student_data
                            )
                            if response.status_code == 201:
                                st.success("Student added successfully!")
                                # Create initial fee record
                                fee_data = {
                                    "student_name": name,
                                    "total_fees": fee_payable,
                                    "amount_paid": 0,
                                    "balance": fee_payable,
                                }
                                fee_response = requests.post(f"{BASE_URL}/fees", json=fee_data)
                                if fee_response.status_code == 201:
                                    st.success("Initial fee record created successfully!")
                                else:
                                    st.error("Error creating initial fee record")
                                
                                st.rerun()
                            else:
                                error_message = response.json().get(
                                    "error", "Unknown error"
                                )
                                st.error(f"Error adding student: {error_message}")
                                st.rerun()

    with tab2:
        daycare_tab1, daycare_tab2 = st.tabs(["View Children", "Add child"])

        with daycare_tab1:
            # Automatically fetch and display students
            daycare = fetch_data("daycare")
            if daycare:
                # Convert list of daycare dictionaries to a Dataframe
                df = pd.DataFrame(
                    daycare,
                    columns=[
                        "name",
                        "parent_1_name",
                        "parent_1_phone",
                        "parent_2_name",
                        "parent_2_phone",
                        "payment_mode",
                        "option",
                        "fee_payable",
                        "fee_paid",
                        "balance",
                        "status",
                    ],
                )
                st.dataframe(df, use_container_width=True)
            else:
                st.write("No children to display.")

        with daycare_tab2:
            # Add daycare form
            st.write("Add a new child:")
            with st.form(key="daycare_form"):
                name = st.text_input("Child's Name")
                parent_1_name = st.text_input("Parent 1 Name")
                parent_1_phone = st.text_input("Parent 1 Phone")
                parent_2_name = st.text_input("Parent 2 Name")
                parent_2_phone = st.text_input("Parent 2 Phone")
                payment_mode = st.selectbox(
                    "Payment mode", ["Daily", "Weekly", "Monthly"]
                )
                option = st.selectbox("Option", ["Home meals", "School meals"])
                fee_payable = st.number_input("Fee Payable")
                submit_button = st.form_submit_button(label="Submit")

                if submit_button:
                    # Form validation
                    if not all(
                        [
                            name,
                            parent_1_name,
                            parent_1_phone,
                            payment_mode,
                            option,
                            fee_payable,
                            
                        ]
                    ):
                        st.error("All fields are required.")
                    else:
                        # Check for duplicates
                        daycare = fetch_data("daycare")
                        if daycare is None:
                            daycare = []
                        duplicate = any(
                            daycare for daycare in daycare if daycare["name"] == name
                        )
                        if duplicate:
                            st.error("This child is already entered.")
                        else:
                            daycare_data = {
                                "name": name,
                                "parent_1_name": parent_1_name,
                                "parent_1_phone": parent_1_phone,
                                "parent_2_name": parent_2_name,
                                "parent_2_phone": parent_2_phone,
                                "payment_mode": payment_mode,
                                "option": option,
                                "fee_payable": fee_payable,
                                "fee_paid": 0, #initialize to 0
                                "balance": fee_payable,
                                "status": "Unpaid",
                            }
                            response = requests.post(
                                f"{BASE_URL}/daycare", json=daycare_data
                            )
                            if response.status_code == 201:
                                st.success("Child added successfully!")
                                st.session_state.show_form = False
                                st.rerun()
                            else:
                                error_message = response.json().get(
                                    "error", "Unknown error"
                                )
                                st.error(f"Error adding child: {error_message}")
                                st.rerun()

    with tab3:
        students = fetch_data("students")
        daycare_data = fetch_data("daycare")

        total_students = 0
        total_children = 0

        students_per_class = pd.Series(dtype=int)

        if students:
            # calctulate number of students
            total_students = len(students)

            # calculate number of students per class
            df_students = pd.DataFrame(students)
            students_per_class = df_students["class_name"].value_counts()

        if daycare_data:
            # calculate total number of daycare children
            total_children = len(daycare_data)

            # Add daycare children as their own class
            daycare_series = pd.Series(total_children, index=["Daycare"])
            students_per_class = pd.concat([students_per_class, daycare_series])

            # create a pie chart
            students_per_class_df = students_per_class.reset_index()
            students_per_class_df.columns = [
                "Class",
                "Count",
            ]  # rename columns for clarity
            fig = px.pie(
                students_per_class_df,
                names="Class",
                values="Count",
                title="Disribution of Students per class",
            )
            st.plotly_chart(fig)

        # display students and daycare in one line
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Total Students : {total_students}")
        with col2:
            st.write(f"Total Daycare Children : {total_children}")

        if not students_per_class.empty:
            st.write("Total Students per Class : ")
            st.write(students_per_class)


# Fee Management Section
if choice == "Fees":
    st.markdown(
        "<div class='section-header'>Fee Management</div>", unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["Records", "Analytics"])

    with tab1:
        # Automatically fetch and display fee records
        fees = fetch_data("fees")
        if fees:
            # Convert list of fee dictionaries to a Dataframe
            df = pd.DataFrame(
                fees,
                columns=[
                    "student_name",
                    "total_fees",
                    "amount_paid",
                    "balance",
                    "remarks",
                ],
            )
            st.dataframe(df, use_container_width=True)
        else:
            st.write("No Fee records to display.")

    with tab2:
        # fetch fees data
        fees = fetch_data("fees")
        daycare = fetch_data("daycare")

        if fees:
            df = pd.DataFrame(fees)

            # ensure the columns are numeric
            df["amount_paid"] = pd.to_numeric(df["amount_paid"], errors="coerce")
            df["balance"] = pd.to_numeric(df["balance"], errors="coerce")
            df["total_fees"] = pd.to_numeric(df["total_fees"], errors="coerce")

            # calculations
            total_paid = df["amount_paid"].sum()
            total_balance = df["balance"].sum()
            fees_expected = df["total_fees"].sum()

            # create a pie-chart
            fig = px.pie(
                names=["Amount Paid", "Balance"],
                values=[total_paid, total_balance],
                title="Student Fees",
            )
            st.plotly_chart(fig)

            # create columns
            col1, col2 = st.columns(2)

            with col1:
                # display calculatons
                st.write(f"Total Fee Expected : {fees_expected:,.2f}")
                st.write(f"Total Amount Paid : {total_paid:,.2f}")
                st.write(f"Total Fee Balance : {total_balance:,.2f}")

            with col2:
                if daycare:
                    df = pd.DataFrame(daycare)

                    df["fee_paid"] = pd.to_numeric(df["fee_paid"], errors="coerce")
                    df["balance"] = pd.to_numeric(df["balance"], errors="coerce")

                    # calculations
                    fee_paid = df["fee_paid"].sum()
                    total_balance = df["balance"].sum()

                    # display calculatons
                    st.write(f"Daycare Total Collected : {fee_paid:,.2f}")
                    st.write(f"Daycare Monthly balance : {total_balance:,.2f}")


# Expenditure Management Section
if choice == "Expenditure":
    st.markdown(
        "<div class='section-header'>Expenditure Management</div>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Expenses", "Add Expenses", "Analysis"])

    with tab1:
        # Automatically fetch and display expenditures
        expenditures = fetch_data("expenditures")
        if expenditures:
            # Convert list of expenditure dictionaries to a Dataframe
            df = pd.DataFrame(
                expenditures, columns=["date", "item", "category", "vendor", "amount"]
            )
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%a, %d %b %Y")

            st.dataframe(df, use_container_width=True)
        else:
            st.write("No expenditures to display.")

    with tab2:
        exp = fetch_data("expenditures")
        categories = [""]
        vendors = [""]

        if exp:
            # Use set() to get unique categories and vendors from the expenditures table
            unique_categories = set(expense["category"] for expense in exp if expense["category"])
            unique_vendors = set(expense["vendor"] for expense in exp if expense["vendor"])
            
            categories.extend(sorted(unique_categories))
            vendors.extend(sorted(unique_vendors))
            st.write("Add new Expenditure")
        with st.form(key="expenditure_form"):
            date = st.date_input("Date")
            item = st.text_input("Item")
            category = st.selectbox("Category", options=categories)
            vendor = st.selectbox("Vendor", options=vendors)
            amount = st.number_input("Amount")
            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                # Form validation
                if not all([date, item, category, vendor, amount is not None]):
                    st.error("All fields are required.")
                else:
                    formatted_date = date.strftime("%a, %d %b %Y")

                    # Fetch existing expenditures to check for duplicates
                    expenditures = fetch_data("expenditures")
                    df = pd.DataFrame(expenditures)

                    duplicate_check = df[
                        (df["date"] == formatted_date)
                        & (df["item"] == item)
                        & (df["amount"] == float(amount))
                    ]
                    if not duplicate_check.empty:
                        st.error( "Duplicate expenditure record found. Please check the details.")

                    else:
                        expenditure_data = {
                            "date": formatted_date,
                            "item": item,
                            "category": category,
                            "vendor": vendor,
                            "amount": amount,
                        }
                        
                        response = requests.post(
                            f"{BASE_URL}/expenditures", json=expenditure_data
                        )
                        if response.status_code == 201:
                            st.success("Expenditure added successfully!")
                            st.rerun()
                        elif response.status_code == 409:
                            st.error("Duplicate entry. This expenditure already exists.")
                        else:
                            error_message = response.json().get('error', 'Unknown error occurred')
                            st.error(f"Error adding expenditure: {error_message}")
                            st.rerun()

    with tab3:
        expenditures = fetch_data("expenditures")
        if expenditures:
            df = pd.DataFrame(
                expenditures, columns=["date", "item", "category", "vendor", "amount"]
            )
            df["date"] = pd.to_datetime(df["date"])
            df["month"] = df["date"].dt.to_period("M").astype(str)
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

            # Create bar chart for expenditures per category
            fig_category = px.bar(
                df.groupby("category")["amount"].sum().reset_index(),
                x="category",
                y="amount",
                title="Expenditures per Category",
            )
            st.plotly_chart(fig_category)

            # Calculate the amount per category
            amount_per_category = (
                df.groupby("category")["amount"].sum().sort_values(ascending=False)
            )
            st.write("Amount per Category:")
            st.write(amount_per_category)

            # Create bar chart for expenditures per vendor
            fig_vendor = px.bar(
                df.groupby("vendor")["amount"].sum().reset_index(),
                x="vendor",
                y="amount",
                title="Expenditures per Vendor",
            )
            st.plotly_chart(fig_vendor)

            # Calculate the amount per vendor
            amount_per_vendor = (
                df.groupby("vendor")["amount"].sum().sort_values(ascending=False)
            )
            st.write("Amount per Vendor:")
            st.write(amount_per_vendor)

            # Create bar chart for expenditures per month
            fig_month = px.bar(
                df.groupby("month")["amount"].sum().reset_index(),
                x="month",
                y="amount",
                title="Expenditures per Month",
            )
            st.plotly_chart(fig_month)

            # Calculate the total amount per month
            total_amount_per_month = (
                df.groupby("month")["amount"].sum().sort_values(ascending=False)
            )
            st.write("Total Amount per Month:")
            st.write(total_amount_per_month)

            # Calculate the amount per category for each month
            amount_per_category_month = (
                df.groupby(["month", "category"])["amount"].sum().unstack().fillna(0)
            )
            st.write("Amount per Category per Month:")
            st.write(amount_per_category_month)

            # Responsive chart with user inputs for X and Y axes
            st.write("Create Custom Chart")
            x_axis = st.selectbox("Select X-axis variable", options=df.columns, index=5)
            y_axis = st.selectbox("Select Y-axis variable", options=["amount"], index=0)

            fig_custom = px.bar(
                df.groupby(x_axis)[y_axis].sum().reset_index(),
                x=x_axis,
                y=y_axis,
                title=f"Expenditures by {x_axis}",
            )
            st.plotly_chart(fig_custom)

            # Customizable input for category-wise item expenditure
            st.write("Category-wise Item Expenditure")
            category_option = st.selectbox(
                "Select Category", options=amount_per_category.index
            )
            category_items = (
                df[df["category"] == category_option]
                .groupby("item")["amount"]
                .sum()
                .sort_values(ascending=False)
            )
            st.write(f"Items in {category_option} Category:")
            st.write(category_items)

            # Customizable input for vendor-wise item expenditure
            st.write("Vendor-wise Item Expenditure")
            vendor_option = st.selectbox(
                "Select Vendor", options=amount_per_vendor.index
            )
            vendor_items = (
                df[df["vendor"] == vendor_option]
                .groupby("item")["amount"]
                .sum()
                .sort_values(ascending=False)
            )
            st.write(f"Items from {vendor_option}:")
            st.write(vendor_items)
        else:
            st.write("No expenditure data to analyze.")


# Activity Management Section
if choice == "Activities":
    st.markdown(
        "<div class='section-header'>Activity Management</div>", unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["Activities", "Add activity"])

    with tab1:
        # Automatically fetch and display activities
        activities = fetch_data("activities")
        if activities:
            # Convert list of activity dictionaries to a Dataframe
            df = pd.DataFrame(
                activities, columns=["activity_name", "fee_amount", "payment_frequency"]
            )
            st.dataframe(df,use_container_width=True)
        else:
            st.write("No activities to display.")

    with tab2:
        st.write("Add new Activity")
        with st.form(key="activity_form"):
            activity_name = st.text_input("Activity Name")
            payment_frequency = st.selectbox(
                "Payment Frequency", ["Daily", "Weekly", "Monthly", "termly"]
            )
            fee_amount = st.number_input("Fee Amount")
            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                # Form validation
                if not all([activity_name, payment_frequency, fee_amount is not None]):
                    st.error("All fields are required.")
                else:
                    activity_data = {
                        "activity_name": activity_name,
                        "payment_frequency": payment_frequency,
                        "fee_amount": fee_amount,
                    }
                    response = requests.post(
                        f"{BASE_URL}/activities", json=activity_data
                    )
                    if response.status_code == 201:
                        st.success("Activity added successfully!")
                        st.session_state.show_form = False
                        st.rerun()
                    else:
                        st.error("Error adding activity")
                        st.rerun()


# Student Activity Management Section
if choice == "Student Activity":
    st.markdown(
        "<div class='section-header'>Student Activity Management</div>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Student Activities", "Add Std Activity", "Analysis"])

    with tab1:
        # Automatically fetch and display student activities
        student_activities = fetch_data("student_activities")
        if student_activities:
            # Convert list of expenditure dictionaries to a Dataframe
            df = pd.DataFrame(
                student_activities, columns=["student_name", "activity_name"]
            )
            st.dataframe(df)
        else:
            st.write("No students activities to display.")

    with tab2:
        students = fetch_data("students")
        daycare_data = fetch_data("daycare")

        student_names = [""]
        if students:
            student_names.extend([student["name"] for student in students])
        if daycare_data:
            student_names.extend([child["name"] for child in daycare_data])

        # Add student activity form
        st.write("Add new Student Activity")
        with st.form(key="student_activity_form"):
            student_name_input = st.selectbox("Student Name", options=student_names)
            activity_name = st.text_input("Activity Name")
            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                # Form validation
                if not all([student_name_input, activity_name]):
                    st.error("All fields are required.")
                else:
                    student_activity_data = {
                        "student_name": student_name_input,
                        "activity_name": activity_name,
                    }
                    response = requests.post(
                        f"{BASE_URL}/student_activities", json=student_activity_data
                    )
                    if response.status_code == 201:
                        st.success("Student activity added successfully!")
                        st.session_state.show_form = False
                        st.rerun()
                    else:
                        st.error("Error adding student activity")
                        st.rerun()

    with tab3:
        student_activites = fetch_data("student_activities")
        if student_activities:
            df = pd.DataFrame(
                student_activities, columns=["student_name", "activity_name"]
            )

            # calculate the number of students per activity
            students_per_activity = df["activity_name"].value_counts().reset_index()
            students_per_activity.columns = ["activity_name", "count"]

            # create a pie chart
            fig = px.pie(
                students_per_activity,
                values="count",
                names="activity_name",
                title="Distribution of students per activity",
            )
            st.plotly_chart(fig)

            st.write("Number of students per activity:")
            st.write(students_per_activity)

        else:
            st.write("No student activity data to analyze")


# Activity Participation Management Section
if choice == "Activity Participation":
    st.markdown(
        "<div class='section-header'>Activity Participation Management</div>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Participation records", "Add record", "Analysis"])

    with tab1:
        # Automatically fetch and display participation records
        participations = fetch_data("activity_participation")
        if participations:
            # Convert list of participation dictionaries to a Dataframe
            df = pd.DataFrame(
                participations,
                columns=[
                    "student_name",
                    "activity_name",
                    "term",
                    "frequency",
                    "status",
                    "date_paid_for",
                    "amount_paid",
                    "balance",
                ],
            )
            st.dataframe(df,use_container_width=True)
        else:
            st.write("No participations to display.")

    with tab2:
        students = fetch_data("students")
        daycare_data = fetch_data("daycare")

        student_names = [""]
        if students:
            student_names.extend([student["name"] for student in students])
        if daycare_data:
            student_names.extend([child["name"] for child in daycare_data])

        with st.form(key="participation_form"):
            student_name_input = st.selectbox("Student Name", options=student_names)
            activity_name = st.text_input("Activity Name")
            term = st.number_input("Term", min_value=1)
            frequency = st.selectbox(
                "Frequency", ["Daily", "Weekly", "Monthly", "termly"]
            )
            status = st.selectbox(
                "Status", ["Complete", "Incomplete", "Paid", "Unpaid"]
            )
            date_paid_for = st.date_input("Date Paid For")
            amount_paid = st.number_input("Amount Paid")
            balance = st.number_input("Balance")
            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                # Form validation
                if not all(
                    [
                        student_name_input,
                        activity_name,
                        term,
                        frequency,
                        status,
                        date_paid_for,
                        amount_paid is not None,
                        balance is not None,
                    ]
                ):
                    st.error("All fields are required.")
                else:
                    participation_data = {
                        "student_name": student_name_input,
                        "activity_name": activity_name,
                        "term": term,
                        "frequency": frequency,
                        "status": status,
                        "date_paid_for": date_paid_for.strftime("%Y-%m-%d"),
                        "amount_paid": amount_paid,
                        "balance": balance,
                    }
                    response = requests.post(
                        f"{BASE_URL}/activity_participation", json=participation_data
                    )
                    if response.status_code == 201:
                        st.success("Participation record added successfully!")
                        st.rerun()
                    else:
                        st.error("Error adding participation record")
                        st.rerun()

    with tab3:
        participation_records = fetch_data("activity_participation")
        if participation_records:
            df = pd.DataFrame(
                participation_records,
                columns=[
                    "student_name",
                    "activity_name",
                    "term",
                    "frequency",
                    "status",
                    "date_paid_for",
                    "amount_paid",
                    "balance",
                ],
            )

            # Convert date_paid_for to datetime, handle errors gracefully
            df["date_paid_for"] = pd.to_datetime(df["date_paid_for"], errors="coerce")

            # Drop rows with invalid dates
            df = df.dropna(subset=["date_paid_for"])

            # Convert date_paid_for to datetime
            df["month"] = df["date_paid_for"].dt.to_period("M").astype(str)
            df["amount_paid"] = pd.to_numeric(df["amount_paid"], errors="coerce")
            df["balance"] = pd.to_numeric(df["balance"], errors="coerce")

            # calculate the amount paid per activity per month
            amount_paid_per_activity_month = (
                df.groupby(["month", "activity_name"])["amount_paid"]
                .sum()
                .reset_index()
            )
            amount_paid_per_activity_month["month"] = amount_paid_per_activity_month[
                "month"
            ].astype(str)

            # calculate the total amount paid per month
            amount_paid_per_month = (
                df.groupby("month")["amount_paid"].sum().reset_index()
            )
            amount_paid_per_month["month"] = amount_paid_per_month["month"].astype(str)

            # create a stacked bar chart
            fig = px.bar(
                amount_paid_per_activity_month,
                x="month",
                y="amount_paid",
                color="activity_name",
                title="Amount paid per month per activity",
                labels={
                    "amount_paid": "Amount Paid",
                    "month": "Month",
                    "activity_name": "Activity",
                },
            )
            st.plotly_chart(fig)

            # display the result
            st.write("Amount Paid per Activity per Month:")
            st.write(amount_paid_per_activity_month)

            # display the result
            st.write("Total Amount Paid per Month")
            st.write(amount_paid_per_month)

        else:
            st.write("No participation data to analyze.")


# Income Management Section
if choice == "Income":
    st.markdown(
        "<div class='section-header'>Income Management</div>", unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs(["Income records", "Add income", "Analysis"])

    with tab1:
        # Automatically fetch and display income records
        income_records = fetch_data("income")
        if income_records:
            # Convert list of income dictionaries to a Dataframe
            df = pd.DataFrame(
                income_records, columns=["student_name", "source", "amount", "date"]
            )
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%a, %d %b %Y")

            st.dataframe(df,use_container_width=True)
        else:
            st.write("No income records to display.")
    with tab2:
        students = fetch_data("students")
        daycare_data = fetch_data("daycare")

        
        student_names = [""]

        if students:
            student_names.extend([student["name"] for student in students])
        if daycare_data:
            student_names.extend([child["name"] for child in daycare_data])
         
        # Add income record form
        st.write("Add new income record")
        with st.form(key="income_form"):
            student_name_input = st.selectbox("Student Name", options=student_names)
            source = st.selectbox("Source", ['Fees', 'Daycare','Swimming','Transport', 'Uniform', 'Graduation', 'Educational Trip', 'School Activity'], index=None)
            amount = st.number_input("Amount")
            date = st.date_input("Date")
            submit_button = st.form_submit_button(label="Submit")

            if submit_button:
                # Form validation
                if not all([student_name_input, source, amount is not None, date]):
                    st.error("All fields are required.")
                
                else:
                    formatted_date = date.strftime("%a, %d %b %Y")

                    # Fetch existing expenditures to check for duplicates
                    income = fetch_data("income")
                    if income:
                        df = pd.DataFrame(income)
                        
                        # Check if 'date' column exists
                        if 'date' in df.columns:
                            duplicate_check = df[
                                (df["date"] == formatted_date)
                                & (df["source"] == source)
                                & (df["amount"] == float(amount))
                                & (df["student_name"] == student_name_input)
                            ]
                            if not duplicate_check.empty:
                                st.error("Duplicate income record found. Please check the details.")
                                st.stop()
                        else:
                            st.warning("Unable to check for duplicates due to missing date information.")

                    income_data = {
                            "student_name": student_name_input,
                            "source": source,
                            "amount": amount,
                            "date": formatted_date,
                        }
                    #First add the income record
                    income_response = requests.post(f"{BASE_URL}/income", json=income_data)
                    if income_response.status_code == 201:
                        response_data = income_response.json()
                        st.success(response_data['message'])
                        
                        if 'updated_fee' in response_data:                                
                                st.write(response_data['updated_fee'])
                        
                        # Use st.rerun() to refresh the page
                        st.rerun()
                        
                    elif income_response.status_code == 409:
                        st.error("Duplicate entry. This income record already exists.")
                        st.rerun()
                    else:
                        st.error("Error adding income record")
                        st.rerun()                                   
    with tab3:
        st.write("Income & Profit Analysis")
        income_records = fetch_data("income")
        expenditure_records = fetch_data("expenditures")

        if income_records:
            df = pd.DataFrame(
                income_records, columns=["student_name", "source", "amount", "date"]
            )

            # Convert date to datetime, handle errors gracefully
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

            # Drop rows with invalid dates
            df = df.dropna(subset=["date"])

            # Calculate the total amount received per month per source
            df["month"] = df["date"].dt.to_period("M").astype(str)
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
            amount_per_month_source = (
                df.groupby(["month", "source"])["amount"].sum().reset_index()
            )
            amount_per_month_source["month"] = amount_per_month_source["month"].astype(
                str
            )

            # Calculate the total amount received per source
            total_amount_per_source = df.groupby("source")["amount"].sum().reset_index()

            # Create a stacked bar chart
            fig = px.bar(
                amount_per_month_source,
                x="month",
                y="amount",
                color="source",
                title="Amount Received per Month per Source",
                labels={
                    "amount": "Amount Received",
                    "month": "Month",
                    "source": "Source",
                },
            )
            st.plotly_chart(fig)

            # Display the results below the graph
            st.write("Total Amount Received per Source:")
            st.write(total_amount_per_source)

            st.write("Total Amount Received per Month per Source:")
            st.write(amount_per_month_source)
        else:
            st.write("No income data to analyze.")
        if income_records and expenditure_records:
            income_df = pd.DataFrame(income_records, columns=["student_name", "source", "amount", "date"])
            expenditure_df = pd.DataFrame(expenditure_records, columns=["date", "item", "category", "vendor", "amount"])

            # Convert date to datetime and amount to numeric for both dataframes
            for df in [income_df, expenditure_df]:
                df["date"] = pd.to_datetime(df["date"], errors="coerce")
                df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
                df["month"] = df["date"].dt.to_period("M").astype(str)

            # Group by month and sum the amounts
            monthly_income = income_df.groupby("month")["amount"].sum().reset_index()
            monthly_expenditure = expenditure_df.groupby("month")["amount"].sum().reset_index()

            # Merge income and expenditure data
            profit_analysis = pd.merge(monthly_income, monthly_expenditure, on="month", suffixes=('_income', '_expenditure'))
            
            # Calculate profit
            profit_analysis['profit'] = profit_analysis['amount_income'] - profit_analysis['amount_expenditure']

            # Display the profit analysis
            st.write("Monthly Profit Analysis:")
            st.dataframe(profit_analysis)

            # Create a line chart for profit analysis
            fig = px.line(profit_analysis, x="month", y=["amount_income", "amount_expenditure", "profit"],
                        title="Monthly Income, Expenditure, and Profit",
                        labels={"value": "Amount", "month": "Month", "variable": "Category"},
                        color_discrete_map={"amount_income": "green", "amount_expenditure": "red", "profit": "blue"})
            st.plotly_chart(fig)

            # Calculate and display total profit
            total_income = income_df["amount"].sum()
            total_expenditure = expenditure_df["amount"].sum()
            total_profit = total_income - total_expenditure

            # Create a DataFrame for the summary
            summary_df = pd.DataFrame({
                'Category': ['Total Income', 'Total Expenditure', 'Total Profit'],
                'Amount (Ksh.)': [total_income, total_expenditure, total_profit]
            })

            # Format the 'Amount' column
            summary_df['Amount (Ksh.)'] = summary_df['Amount (Ksh.)'].apply(lambda x: f"{x:,.2f}")

            # Display the summary table
            st.write("Financial Summary:")
            st.table(summary_df.set_index('Category'))
        else:
            st.write("Insufficient data for profit analysis.")


