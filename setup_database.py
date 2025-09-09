import mysql.connector
from mysql.connector import errorcode

# --- F1 2020 DATA ---
# NEW: Added Country Code, Birthplace, Championships, Podiums
teams_data = [
    (1, 'Mercedes-AMG Petronas F1 Team', 'Brackley, United Kingdom'), (2, 'Scuderia Ferrari', 'Maranello, Italy'),
    (3, 'Red Bull Racing Honda', 'Milton Keynes, United Kingdom'), (4, 'McLaren F1 Team', 'Woking, United Kingdom'),
    (5, 'Alpine F1 Team (Renault)', 'Enstone, United Kingdom'), (6, 'Scuderia AlphaTauri Honda', 'Faenza, Italy'),
    (7, 'Aston Martin Cognizant F1 Team (Racing Point)', 'Silverstone, United Kingdom'), (8, 'Alfa Romeo Racing ORLEN', 'Hinwil, Switzerland'),
    (9, 'Haas F1 Team', 'Kannapolis, United States'), (10, 'Williams Racing', 'Grove, United Kingdom'),
]
drivers_data = [
    (1, 'Lewis Hamilton', 44, 'British', 'gb', 'Stevenage, England', 7, 165, 1),
    (2, 'Valtteri Bottas', 77, 'Finnish', 'fi', 'Nastola, Finland', 0, 56, 1),
    (3, 'Charles Leclerc', 16, 'Monegasque', 'mc', 'Monte Carlo, Monaco', 0, 12, 2),
    (4, 'Sebastian Vettel', 5, 'German', 'de', 'Heppenheim, Germany', 4, 121, 2),
    (5, 'Max Verstappen', 33, 'Dutch', 'nl', 'Hasselt, Belgium', 0, 42, 3),
    (6, 'Alexander Albon', 23, 'Thai', 'th', 'London, England', 0, 2, 3),
    (7, 'Carlos Sainz', 55, 'Spanish', 'es', 'Madrid, Spain', 0, 2, 4),
    (8, 'Lando Norris', 4, 'British', 'gb', 'Bristol, England', 0, 1, 4),
    (9, 'Daniel Ricciardo', 3, 'Australian', 'au', 'Perth, Australia', 0, 31, 5),
    (10, 'Esteban Ocon', 31, 'French', 'fr', 'Évreux, France', 0, 1, 5),
    (11, 'Pierre Gasly', 10, 'French', 'fr', 'Rouen, France', 0, 2, 6),
    (12, 'Daniil Kvyat', 26, 'Russian', 'ru', 'Ufa, Russia', 0, 3, 6),
    (13, 'Sergio Pérez', 11, 'Mexican', 'mx', 'Guadalajara, Mexico', 0, 10, 7),
    (14, 'Lance Stroll', 18, 'Canadian', 'ca', 'Montreal, Canada', 0, 3, 7),
    (15, 'Kimi Räikkönen', 7, 'Finnish', 'fi', 'Espoo, Finland', 1, 103, 8),
    (16, 'Antonio Giovinazzi', 99, 'Italian', 'it', 'Martina Franca, Italy', 0, 0, 8),
    (17, 'Romain Grosjean', 8, 'French', 'fr', 'Geneva, Switzerland', 0, 10, 9),
    (18, 'Kevin Magnussen', 20, 'Danish', 'dk', 'Roskilde, Denmark', 0, 1, 9),
    (19, 'George Russell', 63, 'British', 'gb', 'King\'s Lynn, England', 0, 1, 10),
    (20, 'Nicholas Latifi', 6, 'Canadian', 'ca', 'Montreal, Canada', 0, 0, 10),
]
races_data = [
    ('Australian Grand Prix', 'Australia'), ('Bahrain Grand Prix', 'Bahrain'), ('Vietnamese Grand Prix', 'Vietnam'),
    ('Chinese Grand Prix', 'China'), ('Dutch Grand Prix', 'Netherlands'), ('Spanish Grand Prix', 'Spain'),
    ('Monaco Grand Prix', 'Monaco'), ('Azerbaijan Grand Prix', 'Azerbaijan'), ('Canadian Grand Prix', 'Canada'),
    ('French Grand Prix', 'France'), ('Austrian Grand Prix', 'Austria'), ('British Grand Prix', 'Great Britain'),
    ('Hungarian Grand Prix', 'Hungary'), ('Belgian Grand Prix', 'Belgium'), ('Italian Grand Prix', 'Italy'),
    ('Singapore Grand Prix', 'Singapore'), ('Russian Grand Prix', 'Russia'), ('Japanese Grand Prix', 'Japan'),
    ('United States Grand Prix', 'USA'), ('Mexican Grand Prix', 'Mexico'), ('Brazilian Grand Prix', 'Brazil'),
    ('Abu Dhabi Grand Prix', 'UAE')
]

# --- MAIN SCRIPT ---
def setup_database():
    config = {'user': 'root', 'password': 'root', 'host': '127.0.0.1', 'database': 'f1_career_db'}
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print("Successfully connected to MySQL database.")

        # --- Drop existing tables to start fresh ---
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute("DROP TABLE IF EXISTS results, races, driver_standings, constructor_standings, drivers, teams;")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        print("Dropped all existing tables.")

        # --- Recreate tables with the new structure ---
        cursor.execute("""
            CREATE TABLE teams (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                base VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE drivers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                number INT,
                nationality VARCHAR(255),
                country_code VARCHAR(10),
                birthplace VARCHAR(255),
                championships INT DEFAULT 0,
                podiums INT DEFAULT 0,
                team_id INT,
                is_player BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL
            );
        """)
        cursor.execute("CREATE TABLE driver_standings ( driver_id INT PRIMARY KEY, points INT DEFAULT 0, wins INT DEFAULT 0, FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE);")
        cursor.execute("CREATE TABLE constructor_standings ( team_id INT PRIMARY KEY, points INT DEFAULT 0, wins INT DEFAULT 0, FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE);")
        cursor.execute("CREATE TABLE races ( id INT AUTO_INCREMENT PRIMARY KEY, track_name VARCHAR(255) NOT NULL UNIQUE, country VARCHAR(255));")
        cursor.execute("""
            CREATE TABLE results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                race_id INT,
                driver_id INT,
                position INT,
                points_scored INT,
                fastest_lap BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (race_id) REFERENCES races(id) ON DELETE CASCADE,
                FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE
            );
        """)
        print("Successfully recreated all tables with new structure.")

        # --- Populate Tables ---
        cursor.executemany("INSERT INTO teams (id, name, base) VALUES (%s, %s, %s)", teams_data)
        cursor.executemany("INSERT INTO drivers (id, name, number, nationality, country_code, birthplace, championships, podiums, team_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", drivers_data)
        cursor.executemany("INSERT INTO races (track_name, country) VALUES (%s, %s)", races_data)
        
        # --- Initialize Standings ---
        driver_ids = [d[0] for d in drivers_data]
        cursor.executemany("INSERT INTO driver_standings (driver_id) VALUES (%s)", [(id,) for id in driver_ids])
        team_ids = [t[0] for t in teams_data]
        cursor.executemany("INSERT INTO constructor_standings (team_id) VALUES (%s)", [(id,) for id in team_ids])
        
        conn.commit()
        print("Database setup complete. All tables populated and initialized.")

    except mysql.connector.Error as err:
        print(f"DATABASE ERROR: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed.")

if __name__ == '__main__':
    setup_database()

