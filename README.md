F1 2020 Two-Player Career Tracker
This web application is a companion for the F1 2020 video game, allowing two players to manage a shared career mode. It provides a full suite of tools to set up custom drivers, track race-by-race results, and view live, auto-calculated championship standings.

This project was built with a Python and Flask backend, a MySQL database for data persistence, and a clean, modern HTML/CSS/JS frontend for a great user experience.

Features
Custom Career Setup: Create a custom team and two player-controlled drivers with unique names, numbers, and nationalities.

Dynamic Results Entry: Submit the full 22-driver finishing order for any race on the F1 2020 calendar.

Automatic Point Calculation: The system automatically assigns points based on the official F1 system (25 for 1st, 18 for 2nd, etc.), including a bonus point for the fastest lap.

Live Championship Standings: View automatically sorted tables for both the Driver's and Constructor's championships that update after every race.

Rich Driver Profiles: View detailed pages for every driver, including their biography, career accomplishments, and a dynamic performance chart visualizing their finishing positions throughout the season.

Full Career Reset: A robust reset feature allows you to clear all player data and race results to start a fresh season.

Technology Stack
Backend: Python 3 with the Flask web framework.

Database: MySQL Server.

Frontend: HTML, CSS, and JavaScript (using Chart.js for data visualization).

WSGI Server: Gunicorn (for production deployment).

Local Setup and Installation
To run this project on your local machine, follow these steps.

Prerequisites:

Python 3 installed on your system.

MySQL Server installed and running.

A tool to manage your MySQL database, like MySQL Workbench.

1. Clone the Repository:

git clone [https://github.com/YOUR_USERNAME/F1_Career_Project.git](https://github.com/YOUR_USERNAME/F1_Career_Project.git)
cd F1_Career_Project

2. Create a Virtual Environment:
It's highly recommended to use a virtual environment to manage project dependencies.

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies:
The requirements.txt file lists all necessary Python packages.

pip install -r requirements.txt

4. Set Up the Database:

Using MySQL Workbench, connect to your local MySQL server and create a new schema named f1_career_db.

Run the provided setup script to create all the necessary tables and populate them with the initial F1 2020 data.

python setup_database.py

5. Configure Environment Variables:
This application uses environment variables to securely manage database credentials. You will need to set the following for your local machine:

DB_HOST: 127.0.0.1

DB_USER: root (or your MySQL username)

DB_PASSWORD: your_mysql_password

DB_NAME: f1_career_db

FLASK_SECRET_KEY: A long, random string for session security.

6. Run the Application:
Once the dependencies are installed and the database is set up, you can start the Flask development server.

flask run

The application will be running at http://127.0.0.1:5000.

Deployment
This application is configured for deployment on cloud platforms like Render, Railway, or Heroku.

General Steps:

Create a Cloud Database: Set up a free MySQL database on a service like PlanetScale or Railway.

Push to GitHub: Make sure your project is uploaded to a GitHub repository.

Create a Web Service: On your chosen hosting platform (e.g., Render), create a new "Web Service" and connect it to your GitHub repository.

Configure Build and Start Commands:

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

Set Environment Variables: In your hosting provider's dashboard, set the same environment variables as in the local setup, but with the credentials for your new cloud database.