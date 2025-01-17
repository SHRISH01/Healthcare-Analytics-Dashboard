import pandas as pd
from connection import connect_to_db

file_path = "./data/processed/cleaned_data.csv"
data = pd.read_csv(file_path)

# Connect to the database
connection = connect_to_db()
cursor = connection.cursor()

# Insert data into the table
for _, row in data.iterrows():
    sql_query = """
    INSERT INTO healthcare_data (
        name, age, gender, blood_type, medical_condition,
        date_of_admission, doctor, hospital, insurance_provider,
        billing_amount, room_number, admission_type,
        discharge_date, medication, test_results
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_query, tuple(row))
    
connection.commit()
print("Data loaded successfully!")
