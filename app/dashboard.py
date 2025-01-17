import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.queries import get_avg_billing_by_condition
import pandas as pd

# Streamlit App
st.title("Healthcare Analytics Dashboard")

# Fetch data
data = get_avg_billing_by_condition()
df = pd.DataFrame(data)

# Display the results
st.header("Average Billing by Medical Condition")
st.bar_chart(df.set_index('medical_condition'))