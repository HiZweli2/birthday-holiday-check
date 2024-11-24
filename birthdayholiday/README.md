# Django Public Holiday Checker App
## Overview
This web application allows users to input a South African ID (SA ID) number and retrieve information about public holidays on their date of birth. The app decodes the SA ID, extracts details like date of birth, gender, and citizenship, and checks for matching holidays using an external API. The app also saves all records in a local database for future use and analysis.

### Running the App
The app can be run in two ways:

1. Using Docker (Recommended)
This method saves time by avoiding the need to manually set up environment variables and dependencies.

Steps:
Clone the repository onto your local machine:
```
git clone <repository_url>
cd <project_directory>
```

Build the Docker image:
```
sudo docker build -t django-app .
```

Run the Docker container:
```
sudo docker run -p 8000:8000 django-app
```

2. Running Locally
For those who prefer running the app locally, you need to ensure Python 3 and pip are installed on your machine.

Steps:
Clone the repository:
git clone <repository_url>
cd <project_directory>

Install dependencies:
pip3 install -r requirements.txt

Run the Django development server:
python manage.py runserver


App Features
Core Functionality:
SA ID Decoding:

Extracts the user's date of birth, gender, and citizenship status from the inputted ID number.
Public Holiday Lookup:

Uses the Calendarific API to check if there are any public holidays on the user's date of birth.
Database Management:

Saves user records (SA ID details and associated holidays) in the local database.
Automatically tracks the number of times each SA ID has been searched.
Results Display:

Neatly displays all saved information for a specific SA ID, including decoded details and public holidays.
User Interface:
Input Form: Users enter their SA ID number and submit the form to retrieve details.

Results Section: Displays:

Extracted details (date of birth, gender, citizenship status).
Public holidays associated with the user's date of birth (if any).
API Integration:
Integrates with the Calendarific API to fetch public holiday data based on the user's year of birth
