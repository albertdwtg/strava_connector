import time
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd
import requests
from dotenv import set_key

from src.conf import Config

ENV_FILE_PATH = Path("./.env")


class Client:
    """Client to interact with Strava API
    """

    def __init__(self) -> None:
        self.client_id = Config.CLIENT_ID
        self.client_secret = Config.CLIENT_SECRET
        self.refresh_token = Config.REFRESH_TOKEN
        self.athlete_id = Config.ATHLETE_ID

    def get_athlete_id(self) -> int:
        """Function that returns the ID of the athlete

        Returns:
            int: athlete ID
        """
        athlete_id = Config.ATHLETE_ID
        if athlete_id is None:
            endpoint = "https://www.strava.com/api/v3/athlete"
            response = self._run_request(endpoint)
            athlete_id = response["id"]
            set_key(dotenv_path=ENV_FILE_PATH, key_to_set="ATHLETE_ID",
                    value_to_set=str(athlete_id))
        return athlete_id

    def get_athlete_data(self, info: str = None) -> dict:
        """Function that gets all general athlete stats

        Args:
            info (str, optional): Can be "routes", "zones" or "stats". 
            If None, the athlete itself is returned. Defaults to None.

        Returns:
            dict: athlete data
        """
        if info:
            if info.lower() == "zones":
                return self._get_athlete_zones()
            athlete_id = self.get_athlete_id()
            info = "/" + info.lower()
            endpoint = f"https://www.strava.com/api/v3/athletes/{athlete_id}{info}"
        else:
            endpoint = "https://www.strava.com/api/v3/athlete"
        response = self._run_request(endpoint)
        return response

    def _get_athlete_zones(self) -> List:
        """Get heart zones of athlete

        Returns:
            List: List of different heart zones
        """
        endpoint = "https://www.strava.com/api/v3/athlete/zones"
        response = self._run_request(endpoint)
        return response["heart_rate"]["zones"]

    def get_athlete_activities(
        self, after: str = None, 
        before: str = None, 
        per_page: int = None,
        output_format: str = "JSON" 
        ) -> dict:
        """Function that gets all activities of an athlete

        Args:
            after (str, optional): Start date of the list (DD/MM/YYYY). Defaults to None.
            before (str, optional): End date of the list (DD/MM/YYYY). Defaults to None.
            per_page (int, optional): number of elements to retrieve. Defaults to None.
            output_format (str, optional): output desired format. Defaults to JSON.

        Returns:
            dict: all activities in dict format
        """
        params = {}
        if per_page:
            params["per_page"] = per_page
        
        if after:
            params["after"] = int(time.mktime(
                datetime.strptime(after, "%d/%m/%Y").timetuple()))
        
        if before:
            params["before"] = int(time.mktime(
                datetime.strptime(before, "%d/%m/%Y").timetuple()))
        
        endpoint = f"https://www.strava.com/api/v3/athlete/activities"

        response = self._run_request(endpoint, params)
        
        if output_format.upper() == "DF":
            response = pd.json_normalize(response)
        return response

    def get_activity_data(self, activity_id: int, info: str = None) -> List:
        """Get infos about an activity

        Args:
            activity_id (int): ID of the activity to analyze
            info (str, optional): Can be "comments", "laps" or "kudos". 
            If None, the activity itself is returned. Defaults to None.

        Returns:
            List: Infos to return
        """
        if info:
            info = "/" + info.lower()
        endpoint = f"https://www.strava.com/api/v3/activities/{activity_id}{info}"
        response = self._run_request(endpoint)
        return response

    def get_equipment(self, gear_id: str) -> dict:
        """Get info about an equipment

        Args:
            gear_id (str): ID of the equipment to analyze

        Returns:
            dict: equipment infos
        """
        endpoint = f"https://www.strava.com/api/v3/gear/{gear_id}"
        response = self._run_request(endpoint)
        return response

    def _get_access_token(self) -> str:
        """Function to get current access token, based on refresh token

        Returns:
            str: access token in string format
        """
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }
        url = "https://www.strava.com/api/v3/oauth/token"

        response = requests.post(url, params=params)
        access_token = response.json()["access_token"]
        return access_token

    def _run_request(self, endpoint: str, params: dict = None) -> dict:
        """Function to run a get request on an endpoint

        Args:
            endpoint (str): endpoint of the request
            params (dict, optional): params to give to the request. Defaults to None.

        Returns:
            dict: output of the request
        """
        token = self._get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            endpoint, headers=headers, params=params).json()
        return response
