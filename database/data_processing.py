import pandas as pd

# Load the CSV file
file_path = "./data/raw/healthcare_dataset.csv"  
data = pd.read_csv(file_path)

# Standardize column names
data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]

# Format string columns
data['name'] = data['name'].str.title()  # Capitalize names properly
data['medical_condition'] = data['medical_condition'].str.capitalize()
data['test_results'] = data['test_results'].str.capitalize()

# Handle missing or incorrect values
data = data.fillna(method='ffill')  # Forward fill for missing values
data['billing_amount'] = data['billing_amount'].clip(lower=0)  # Ensure no negative billing amounts

# Convert date columns to datetime
data['date_of_admission'] = pd.to_datetime(data['date_of_admission'])
data['discharge_date'] = pd.to_datetime(data['discharge_date'])

data.to_csv("./data/processed/cleaned_data.csv", index=False)
print("Data Stored Successfully")
