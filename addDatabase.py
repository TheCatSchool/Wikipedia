import mysql.connector

def get_db_connection():  # defines the database
    return mysql.connector.connect(
        host="127.0.0.1",
        # host="10.200.14.14",
        user="work",
        # password="123",
        password="",
        database="Wikipedia"
    )

conn = get_db_connection()  # fetch database
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    navn VARCHAR(100) NOT NULL,
    epost VARCHAR(150) NOT NULL,
    sporsmal TEXT NOT NULL,
    opprettet DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)
""")

# Save changes
conn.commit()

print("Table 'brukere' created successfully.")

# Close connection
cursor.close()
conn.close()