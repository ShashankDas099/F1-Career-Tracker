F1 2020 Two-Player Career Tracker
A web application built to create a shared, two-player career mode experience for the F1 2020 video game. This app allows you and a friend to create custom drivers, track race results, and watch the championship standings update in real-time. This application is designed and optimized for a PC/desktop viewing experience.

🎯 How to Use This App
There are two ways to use this application:

1. For Players (The Easy Way)
The easiest way to use this application is to click the public link below. This is a live website that anyone can access.

You do not need a Render account, a GitHub account, or any special software. Just open the link in your web browser!

🔴 Live Demo Link: https://f1-career-tracker.onrender.com

Note: For the best experience, it is highly recommended to use this application on a desktop or laptop computer, as the interface is not optimized for mobile devices.

2. For Developers (Running the Code Locally)
If you are a developer and want to run this project on your own computer to see the code, follow the detailed setup instructions further down this page.

✨ Key Features
🏆 Live Championship Standings: Automatically calculated and sorted tables for both Driver's and Constructor's championships.

👤 Custom Career Setup: Create your own custom team and two player drivers with unique names, numbers, and nationalities.

📊 Dynamic Results Entry: A user-friendly form to submit the full 22-driver finishing order for any race.

🏎️ Rich Driver Profiles: Detailed pages for every driver, including their real-world biography, career stats, and a dynamic performance chart that visualizes their finishing positions throughout your career.

🔄 Full Career Reset: A robust reset feature to clear all player data and race results to start a fresh season with one click.

🛠️ Technology Stack
Backend: Python with the Flask web framework.

Database: MySQL (hosted on Clever Cloud).

Frontend: HTML, CSS, and vanilla JavaScript.

Data Visualization: Chart.js for the dynamic driver performance graphs.

Deployment: Hosted on Render.

🚀 Local Development Setup
Want to run this project on your own computer? Here's how:

Prerequisites:

You must have Python 3 and MySQL Server installed.

1. Set Up the Project Folder
First, clone the project from GitHub and navigate into the folder.

git clone [https://github.com/YourUsername/F1-Career-Tracker.git](https://github.com/YourUsername/F1-Career-Tracker.git)
cd F1-Career-Tracker

2. Install the Required Libraries
This command installs all the necessary Python packages listed in requirements.txt.

pip install -r requirements.txt

3. Create and Populate Your Database

Open MySQL Workbench and create a new, empty database (schema) named f1_career_db.

Run the setup script. This will automatically build all the tables and fill them with the official F1 2020 data.

python setup_database.py

(Note: You may need to edit the config in setup_database.py to match your local MySQL password).

4. Start the Application
Run the following command to start the local web server.

flask run