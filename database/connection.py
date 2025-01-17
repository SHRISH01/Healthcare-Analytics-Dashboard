import mysql.connector

def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",      
        user="root",  
        password="Your Password",
        database="healthcare_db" 
    )
    return connection

if __name__ == "__main__":
    conn = connect_to_db()
    if conn.is_connected():
        print("Connected to MySQL!")
