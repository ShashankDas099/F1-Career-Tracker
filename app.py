from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import errorcode
import os # Import the 'os' library to access environment variables

app = Flask(__name__)
# It's important to set a secret key for flash messages to work
# For production, this should also be an environment variable
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key_for_development')


# --- Production-Ready Database Configuration ---
# The app now reads connection details from environment variables.
# This keeps your password secure and out of the code.
db_config = {
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'root'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'database': os.environ.get('DB_NAME', 'f1_career_db')
}

def get_db_connection():
    """Establishes a connection to the database."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# --- Points system dictionary ---
POINTS_MAP = {
    1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1
}

NATIONALITY_TO_CODE_MAP = {
    'American': 'us', 'Argentine': 'ar', 'Australian': 'au', 'Austrian': 'at', 'Belgian': 'be',
    'Brazilian': 'br', 'British': 'gb', 'Canadian': 'ca', 'Chinese': 'cn', 'Colombian': 'co',
    'Danish': 'dk', 'Dutch': 'nl', 'Finnish': 'fi', 'French': 'fr', 'German': 'de',
    'Hungarian': 'hu', 'Indian': 'in', 'Indonesian': 'id', 'Irish': 'ie', 'Italian': 'it',
    'Japanese': 'jp', 'Malaysian': 'my', 'Mexican': 'mx', 'Monegasque': 'mc', 'New Zealander': 'nz',
    'Polish': 'pl', 'Portuguese': 'pt', 'Russian': 'ru', 'Spanish': 'es', 'Swedish': 'se',
    'Swiss': 'ch', 'Thai': 'th', 'Venezuelan': 've'
}


@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM teams")
        team_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM drivers")
        driver_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return render_template('index.html', team_count=team_count, driver_count=driver_count)
    else:
        return "Error: Could not connect to the database."


@app.route('/drivers')
def drivers_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT drivers.id, drivers.name, drivers.number, drivers.nationality, drivers.country_code, teams.name AS team_name
        FROM drivers
        LEFT JOIN teams ON drivers.team_id = teams.id
        ORDER BY drivers.is_player DESC, teams.id, drivers.name;
    """
    cursor.execute(query)
    all_drivers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('drivers.html', drivers=all_drivers)


@app.route('/driver/<int:driver_id>')
def driver_detail_page(driver_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    bio_query = """
        SELECT d.name, d.number, d.nationality, d.country_code, d.birthplace, d.championships, d.podiums, t.name as team_name
        FROM drivers d
        LEFT JOIN teams t ON d.team_id = t.id
        WHERE d.id = %s
    """
    cursor.execute(bio_query, (driver_id,))
    driver_bio = cursor.fetchone()

    standings_query = "SELECT points, wins FROM driver_standings WHERE driver_id = %s"
    cursor.execute(standings_query, (driver_id,))
    driver_standings = cursor.fetchone()

    results_query = """
        SELECT r.track_name, res.position, res.points_scored, res.fastest_lap
        FROM results res
        JOIN races r ON res.race_id = r.id
        WHERE res.driver_id = %s
        ORDER BY r.id
    """
    cursor.execute(results_query, (driver_id,))
    race_results = cursor.fetchall()
    
    chart_labels = [result['track_name'] for result in race_results]
    chart_data = [result['position'] for result in race_results]
    
    cursor.close()
    conn.close()
    
    return render_template(
        'driver_detail.html', 
        driver=driver_bio, 
        standings=driver_standings, 
        results=race_results,
        chart_labels=chart_labels,
        chart_data=chart_data
    )


@app.route('/setup', methods=['GET', 'POST'])
def setup_page():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        p1_number = request.form['player1_number']
        p2_number = request.form['player2_number']

        if p1_number == p2_number:
            flash('Player 1 and Player 2 cannot have the same car number.', 'error')
            return render_template('setup_career.html', form_data=request.form)

        cursor.execute("SELECT number FROM drivers")
        existing_numbers = [row['number'] for row in cursor.fetchall() if row['number'] is not None]
        
        if int(p1_number) in existing_numbers or int(p2_number) in existing_numbers:
            flash('One of the chosen car numbers is already taken by another driver.', 'error')
            return render_template('setup_career.html', form_data=request.form)

        cursor = conn.cursor()
        reset_player_data(cursor, conn)
        
        team_name = request.form['team_name']
        p1_name = request.form['player1_name']
        p1_nationality = request.form['player1_nationality']
        p1_country_code = NATIONALITY_TO_CODE_MAP.get(p1_nationality.strip())

        p2_name = request.form['player2_name']
        p2_nationality = request.form['player2_nationality']
        p2_country_code = NATIONALITY_TO_CODE_MAP.get(p2_nationality.strip())
        
        cursor.execute("INSERT INTO teams (name, base) VALUES (%s, %s)", (team_name, 'Custom Team'))
        new_team_id = cursor.lastrowid
        
        add_driver_query = """
            INSERT INTO drivers (name, number, nationality, country_code, team_id, is_player) 
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """
        cursor.execute(add_driver_query, (p1_name, p1_number, p1_nationality, p1_country_code, new_team_id))
        p1_id = cursor.lastrowid
        cursor.execute(add_driver_query, (p2_name, p2_number, p2_nationality, p2_country_code, new_team_id))
        p2_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO driver_standings (driver_id, points, wins) VALUES (%s, 0, 0)", (p1_id,))
        cursor.execute("INSERT INTO driver_standings (driver_id, points, wins) VALUES (%s, 0, 0)", (p2_id,))
        cursor.execute("INSERT INTO constructor_standings (team_id, points, wins) VALUES (%s, 0, 0)", (new_team_id,))

        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Career created successfully! Your drivers have been added to the grid.', 'success')
        return redirect(url_for('drivers_page'))

    return render_template('setup_career.html')


def reset_player_data(cursor, conn):
    cursor.execute("SELECT id, team_id FROM drivers WHERE is_player = TRUE")
    players = cursor.fetchall()
    if not players:
        return

    player_ids = [p['id'] for p in players]
    team_ids = list(set([p['team_id'] for p in players if p['team_id'] is not None]))

    if player_ids:
        id_placeholders = ','.join(['%s'] * len(player_ids))
        cursor.execute(f"DELETE FROM driver_standings WHERE driver_id IN ({id_placeholders})", player_ids)
        cursor.execute(f"DELETE FROM drivers WHERE id IN ({id_placeholders})", player_ids)

    if team_ids:
        team_placeholders = ','.join(['%s'] * len(team_ids))
        cursor.execute(f"DELETE FROM constructor_standings WHERE team_id IN ({team_placeholders})", team_ids)
        cursor.execute(f"DELETE FROM teams WHERE id IN ({team_placeholders})", team_ids)

    conn.commit()


@app.route('/reset_career', methods=['POST'])
def reset_career():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    reset_player_data(cursor, conn)

    cursor = conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute("TRUNCATE TABLE results;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    
    cursor.execute("UPDATE driver_standings SET points = 0, wins = 0;")
    cursor.execute("UPDATE constructor_standings SET points = 0, wins = 0;")
    conn.commit()

    cursor.close()
    conn.close()
    
    flash('Career has been completely reset. All race results and player data have been cleared.', 'success')
    return redirect(url_for('index'))


@app.route('/add_result', methods=['GET', 'POST'])
def add_result_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        race_id = request.form.get('race_id')
        fastest_lap_driver_id = request.form.get('fastest_lap_driver_id')
        
        cursor.execute("SELECT * FROM results WHERE race_id = %s", (race_id,))
        if cursor.fetchone():
            flash('A result for this race has already been submitted.', 'error')
            return redirect(url_for('add_result_page'))
            
        positions = {}
        for key, value in request.form.items():
            if key.startswith('position_'):
                driver_id = int(key.split('_')[1])
                positions[driver_id] = int(value)

        if len(positions.values()) != len(set(positions.values())):
            flash('Each driver must have a unique finishing position.', 'error')
            return redirect(url_for('add_result_page'))

        fastest_lap_pos = positions.get(int(fastest_lap_driver_id)) if fastest_lap_driver_id else 99
        if fastest_lap_driver_id and fastest_lap_pos > 10:
            flash('Fastest lap bonus can only be awarded to a driver in the top 10.', 'error')
            return redirect(url_for('add_result_page'))

        cursor = conn.cursor()
        for driver_id, position in positions.items():
            points = POINTS_MAP.get(position, 0)
            has_fastest_lap = (str(driver_id) == fastest_lap_driver_id)
            
            if has_fastest_lap:
                points += 1

            cursor.execute("INSERT INTO results (race_id, driver_id, position, points_scored, fastest_lap) VALUES (%s, %s, %s, %s, %s)", (race_id, driver_id, position, points, has_fastest_lap))
            cursor.execute("UPDATE driver_standings SET points = points + %s WHERE driver_id = %s", (points, driver_id))
            if position == 1:
                cursor.execute("UPDATE driver_standings SET wins = wins + 1 WHERE driver_id = %s", (driver_id,))

        cursor.execute("UPDATE constructor_standings cs SET cs.points = (SELECT SUM(ds.points) FROM driver_standings ds JOIN drivers d ON d.id = ds.driver_id WHERE d.team_id = cs.team_id);")
        cursor.execute("UPDATE constructor_standings cs SET cs.wins = (SELECT SUM(ds.wins) FROM driver_standings ds JOIN drivers d ON d.id = ds.driver_id WHERE d.team_id = cs.team_id);")

        conn.commit()
        cursor.close()
        conn.close()

        flash('Race results submitted successfully!', 'success')
        return redirect(url_for('results_index_page'))

    cursor.execute("SELECT id, track_name FROM races ORDER BY track_name")
    races = cursor.fetchall()
    cursor.execute("SELECT id, name FROM drivers ORDER BY name")
    drivers = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('add_result.html', races=races, drivers=drivers)


@app.route('/results')
def results_index_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT DISTINCT r.id, r.track_name, r.country
        FROM races r
        JOIN results res ON r.id = res.race_id
        ORDER BY r.track_name;
    """
    cursor.execute(query)
    completed_races = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('results_index.html', races=completed_races)


@app.route('/results/<int:race_id>')
def result_detail_page(race_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT track_name FROM races WHERE id = %s", (race_id,))
    race = cursor.fetchone()
    query = """
        SELECT res.position, d.name as driver_name, t.name as team_name, res.points_scored, res.fastest_lap
        FROM results res
        JOIN drivers d ON res.driver_id = d.id
        LEFT JOIN teams t ON d.team_id = t.id
        WHERE res.race_id = %s
        ORDER BY res.position;
    """
    cursor.execute(query, (race_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('result_detail.html', race=race, results=results)


@app.route('/standings')
def standings_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    driver_query = """
        SELECT ds.points, ds.wins, d.name as driver_name, t.name as team_name
        FROM driver_standings ds
        JOIN drivers d ON ds.driver_id = d.id
        LEFT JOIN teams t ON d.team_id = t.id
        ORDER BY ds.points DESC, ds.wins DESC, d.name ASC;
    """
    cursor.execute(driver_query)
    driver_standings = cursor.fetchall()
    
    constructor_query = """
        SELECT cs.points, cs.wins, t.name as team_name
        FROM constructor_standings cs
        JOIN teams t ON cs.team_id = t.id
        ORDER BY cs.points DESC, cs.wins DESC, t.name ASC;
    """
    cursor.execute(constructor_query)
    constructor_standings = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('standings.html', driver_standings=driver_standings, constructor_standings=constructor_standings)


# The default Flask server is for development only. 
# For deployment, a production WSGI server like Gunicorn will run the app.
if __name__ == '__main__':
    # The host='0.0.0.0' makes it accessible on your local network
    app.run(debug=False, host='0.0.0.0')

