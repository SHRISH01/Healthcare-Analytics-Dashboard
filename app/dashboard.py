import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import connect_to_db
from database.queries import get_avg_billing_by_condition

# Streamlit App Configuration
st.set_page_config(page_title="Healthcare Analytics Dashboard", layout="wide")

# Title
st.title("Healthcare Analytics Dashboard")

# Database Connection
try:
    connection = connect_to_db()
    st.success("Database connected successfully!")
except Exception as e:
    st.error(f"Failed to connect to the database: {e}")

# Fetch and Display Data
try:
    st.header("Healthcare Data Insights")
    
    # 1. Average Billing by Medical Condition
    st.subheader("1. Average Billing by Medical Condition")
    data = get_avg_billing_by_condition()
    df_billing = pd.DataFrame(data)
    df_billing.columns = ['medical_condition', 'avg_billing'] 
    
    if not df_billing.empty:
        billing_chart = px.bar(
            df_billing,
            x='medical_condition',
            y='avg_billing',
            color='medical_condition',
            title="Average Billing by Medical Condition",
            labels={'medical_condition': "Medical Condition", 'avg_billing': "Average Billing ($)"},
        )
        billing_chart.update_layout(xaxis_title="Medical Condition", yaxis_title="Average Billing ($)")
        st.plotly_chart(billing_chart, use_container_width=True)
    else:
        st.warning("No data available for visualization.")
    
    # 2. Distribution of Admission Types
    st.subheader("2. Distribution of Admission Types")
    query_admissions = """
        SELECT admission_type, COUNT(*) AS count
        FROM healthcare_data
        GROUP BY admission_type
    """
    df_admissions = pd.read_sql(query_admissions, connection)
    if not df_admissions.empty:
        pie_chart = px.pie(
            df_admissions,
            values='count',
            names='admission_type',
            title="Admission Types Distribution",
        )
        st.plotly_chart(pie_chart, use_container_width=True)
    else:
        st.warning("No data available for Admission Types.")

    # 3. Total Billing by Insurance Provider
    st.subheader("3. Total Billing by Insurance Provider")
    query_insurance = """
        SELECT insurance_provider, SUM(billing_amount) AS total_billing
        FROM healthcare_data
        GROUP BY insurance_provider
        ORDER BY total_billing DESC
    """
    df_insurance = pd.read_sql(query_insurance, connection)
    if not df_insurance.empty:
        insurance_chart = px.bar(
            df_insurance,
            x='insurance_provider',
            y='total_billing',
            color='insurance_provider',
            title="Total Billing by Insurance Provider",
            labels={'insurance_provider': "Insurance Provider", 'total_billing': "Total Billing ($)"},
        )
        insurance_chart.update_layout(xaxis_title="Insurance Provider", yaxis_title="Total Billing ($)")
        st.plotly_chart(insurance_chart, use_container_width=True)
    else:
        st.warning("No data available for Insurance Providers.")
    
    # 4. Average Billing by Age Group
    st.subheader("4. Average Billing by Age Group")
    query_age_group = """
        SELECT 
            CASE 
                WHEN age < 18 THEN 'Child'
                WHEN age BETWEEN 18 AND 35 THEN 'Young Adult'
                WHEN age BETWEEN 36 AND 55 THEN 'Adult'
                ELSE 'Senior'
            END AS age_group,
            AVG(billing_amount) AS avg_billing
        FROM healthcare_data
        GROUP BY age_group
        ORDER BY FIELD(age_group, 'Child', 'Young Adult', 'Adult', 'Senior')
    """
    df_age_group = pd.read_sql(query_age_group, connection)
    if not df_age_group.empty:
        age_chart = px.bar(
            df_age_group,
            x='age_group',
            y='avg_billing',
            color='age_group',
            title="Average Billing by Age Group",
            labels={'age_group': "Age Group", 'avg_billing': "Average Billing ($)"},
        )
        st.plotly_chart(age_chart, use_container_width=True)
    else:
        st.warning("No data available for Age Groups.")

    # 5. Number of Patients by Medical Condition
    st.subheader("5. Number of Patients by Medical Condition")
    query_patient_count = """
        SELECT medical_condition, COUNT(*) AS patient_count
        FROM healthcare_data
        GROUP BY medical_condition
        ORDER BY patient_count DESC
    """
    df_patient_count = pd.read_sql(query_patient_count, connection)
    if not df_patient_count.empty:
        patient_chart = px.bar(
            df_patient_count,
            x='medical_condition',
            y='patient_count',
            color='medical_condition',
            title="Number of Patients by Medical Condition",
            labels={'medical_condition': "Medical Condition", 'patient_count': "Patient Count"},
        )
        st.plotly_chart(patient_chart, use_container_width=True)
    else:
        st.warning("No data available for Patient Counts.")
    
except Exception as e:
    st.error(f"Error fetching or displaying data: {e}")
