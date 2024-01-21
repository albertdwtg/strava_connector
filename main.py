from pprint import pprint
from src import strava

strava_client = strava.Client()
pprint(strava_client.get_athlete_activities(per_page=100, output_format="DF"))
# pprint(strava_client.get_athlete_activities()[2])
# pprint(strava_client.get_activity_data(10556240113))
# pprint(strava_client.get_athlete_data(info = "zones"))
# pprint(strava_client.get_equipment("g14010307"))