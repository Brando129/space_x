from flask_app import app
from flask import render_template
from datetime import datetime
import requests
from pprint import pprint

@app.get('/')
def index():
    return render_template('index.html', all_launches=launches)

@app.template_filter('date_only')
def date_only_filter(s):
    date_object = datetime.strptime(s,"%Y-%m-%dT%H:%M:%S.%fZ")
    return date_object.date()

def fetch_spacex_launches():
    url = 'https://api.spacexdata.com/v4/launches'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def categorize_launches(Launches):
    successful = list(filter(lambda x: x['success'] and not x['upcoming'], Launches))
    failed = list(filter(lambda x: not x['success'] and not x['upcoming'], Launches))
    upcoming = list(filter(lambda x: x['upcoming'], Launches))

    return {
        'successful': successful,
        'failed': failed,
        'upcoming': upcoming
    }

launches = categorize_launches(fetch_spacex_launches())
# print(launches[0])
pprint(launches)