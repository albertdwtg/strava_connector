from src.conf import Config
import requests
from pprint import pprint
from src import strava

strava_client = strava.Client()
# pprint(len(strava_client.get_athlete_activities(per_page=100, before = "01/12/2023")))
pprint(strava_client.get_athlete_activities()[0])