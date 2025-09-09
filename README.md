F1 2020 Two-Player Career Tracker

A web application built to create a shared, two-player career mode experience for the F1 2020 video game. This app allows you and a friend to create custom drivers, track race results, and watch the championship standings update in real-time.



🔴 Live Demo Link: https://your-app-name.onrender.com

(Remember to replace this with your actual Render URL!)



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



🚀 How to Run This Project Locally

Want to run this project on your own computer? Here's how:



Prerequisites:



You must have Python 3 and MySQL Server installed.



1\. Set Up the Project Folder

First, clone the project from GitHub and navigate into the folder.



git clone \[https://github.com/YourUsername/F1-Career-Tracker.git](https://github.com/YourUsername/F1-Career-Tracker.git)

cd F1-Career-Tracker



2\. Install the Required Libraries

This command installs all the necessary Python packages listed in requirements.txt.



pip install -r requirements.txt



3\. Create and Populate Your Database



Open MySQL Workbench and create a new, empty database (schema) named f1\_career\_db.



Run the setup script. This will automatically build all the tables and fill them with the official F1 2020 data.



python setup\_database.py



(Note: You may need to edit the config in setup\_database.py to match your local MySQL password).



4\. Start the Application

Run the following command to start the local web server.



flask run



Your application will be live and accessible at https://www.google.com/search?q=http://127.0.0.1:5000 in your web browser.





\### \*\*Final Step: Update on GitHub\*\*



After you have saved this new `README.md` file, you should upload it to your GitHub profile. This will make your project look much more professional.



1\.  \*\*Open your terminal\*\* in the project folder.

2\.  \*\*Run these commands:\*\*

&nbsp;   ```bash

&nbsp;   git add README.md

&nbsp;   git commit -m "Update README with a more user-friendly design"

&nbsp;   git push

