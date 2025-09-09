import mysql.connector
from mysql.connector import errorcode

# --- F1 2020 Game Calendar Data ---
races_data = [
    ("Australian Grand Prix", "Australia"),
    ("Bahrain Grand Prix", "Bahrain"),
    ("Vietnamese Grand Prix", "Vietnam"),
    ("Chinese Grand Prix", "China"),
    ("Dutch Grand Prix", "Netherlands"),
    ("Spanish Grand Prix", "Spain"),
    ("Monaco Grand Prix", "Monaco"),
    ("Azerbaijan Grand Prix", "Azerbaijan"),
    ("Canadian Grand Prix", "Canada"),
    ("French Grand Prix", "France"),
    ("Austrian Grand Prix", "Austria"),
    ("British Grand Prix", "Great Britain"),
    ("Hungarian Grand Prix", "Hungary"),
    ("Belgian Grand Prix", "Belgium"),
    ("Italian Grand Prix", "Italy"),
    ("Singapore Grand Prix", "Singapore"),
    ("Russian Grand Prix", "Russia"),
    ("Japanese Grand Prix", "Japan"),
    ("United States Grand Prix", "USA"),
    ("Mexico City Grand Prix", "Mexico"),
    ("Brazilian Grand Prix", "Brazil"),
    ("Abu Dhabi Grand Prix", "Abu Dhabi")
]

def populate_races():
    """Connects to MySQL and populates the 'races' table."""
    
    config = {
        'user': 'root',
        'password': 'root', # <-- CHANGE THIS
        'host': '127.0.0.1',
        'database': 'f1_career_db'
    }

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print("Successfully connected to MySQL database.")

        # --- THIS IS THE CORRECTED LOGIC ---
        # 1. Temporarily disable the safety checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        
        # 2. Clear tables in the correct order (child table first)
        cursor.execute("TRUNCATE TABLE results;")
        print("Cleared existing data from 'results' table.")
        cursor.execute("TRUNCATE TABLE races;")
        print("Cleared existing data from 'races' table.")
        
        # 3. Re-enable the safety checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        # --- END OF CORRECTED LOGIC ---

        # Insert new race data
        add_race_query = "INSERT INTO races (track_name, country) VALUES (%s, %s)"
        cursor.executemany(add_race_query, races_data)
        
        conn.commit()
        print(f"Populated 'races' table with {cursor.rowcount} records.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed.")

if __name__ == '__main__':
    populate_races()

