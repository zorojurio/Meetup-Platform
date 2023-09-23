# Meetup Platform
Meetup platform utilizing eventbrite.com using Django.

# Prerequisites
- Python3.9
- Google API Key
- Event Brite API Key

# Steps
- copy env.example to .env
- Get Google API key and add to .env file
- Get Event Brite API Key and add to .env file
- create a virtual env using
  - `python3 -m venv venv`
- activate virtual environment
  - `source venv/bin/activate`
- create super users
  - `python manage.py createsuperuser`
- make migrations
  - `python manage.py migrate`
- Run the project
  - `python manage.py runserver`