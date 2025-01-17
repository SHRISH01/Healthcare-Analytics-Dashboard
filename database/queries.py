from database.connection import connect_to_db

def get_avg_billing_by_condition():
    connection = connect_to_db()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT medical_condition, AVG(billing_amount) AS avg_billing
    FROM healthcare_data
    GROUP BY medical_condition;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return results
