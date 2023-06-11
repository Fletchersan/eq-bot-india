"""Contains 
    class Geocode_API -> API CLASS TO REVERSE GEOCODE A LIST OF LAT LONG DICT OBJECTS
"""

import json
import os
import time
from ast import literal_eval
from typing import Dict, List, Union

import requests
from dotenv import load_dotenv
from requests.structures import CaseInsensitiveDict
from custom_errors import GenericError
load_dotenv()
API_KEY = os.getenv('REVERSE_GEOCODING_API_KEY')



class Geocode_API:
    """API CLASS TO REVERSE GEOCODE A LIST OF LAT LONG DICT OBJECTS"""
    API_KEY_CLAUSE = f"apiKey={API_KEY}"
    REQUEST_URL_ROOT = "https://api.geoapify.com/v1/batch/geocode/reverse"
    MAX_POLL_ATTEMPTS = 5
    def __init__(self, lat_long_list: List[Dict[str, float]]):
        paramter_clause = f"{Geocode_API.API_KEY_CLAUSE}&type=country"
        self.request_url = f"{Geocode_API.REQUEST_URL_ROOT}?{paramter_clause}"
        self.request_body: str = json.dumps(lat_long_list)
        self.headers: CaseInsensitiveDict = CaseInsensitiveDict({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        self.poll_url = self.make_request()
        
    def make_request(self):
        """Makes geocoding request, returns id"""
        response: requests.Response = requests.post(
            self.request_url,
            headers=self.headers,
            json=self.request_body,
            timeout=100
        )
        response_data = json.loads(response.content)
        return response_data['url']
    
    def _poll_for_data_till_available(self):
        is_data_ready = False
        poll_attempt = 1
        while not is_data_ready:
            backoff_time = 5*(2**(poll_attempt-1))
            time.sleep(backoff_time)
            response = requests.get(
                self.poll_url,
                timeout=100
            )
            if response.status_code == 200:
                response_body: Union[List, Dict] = literal_eval(response.content)
                if isinstance(response_body, list):
                    is_data_ready = True
                    return [
                        {
                            'query': res.get('query'),
                            'country': res.get('country', '')
                        } for res in response_body
                    ]
                elif isinstance(response_body, dict) and response_body['status'] != 'pending':
                    raise GenericError("issue while polling api, status is not pending")
                poll_attempt+=1
            if poll_attempt == Geocode_API.MAX_POLL_ATTEMPTS:
                is_data_ready=True
                raise GenericError(f"Made maximum attempt to poll {poll_attempt}")
        def get_country_data(self):
            """polls for geocoding data till it is available and returns country data"""
            return self._poll_for_data_till_available()

# url = f"https://api.geoapify.com/v1/geocode/reverse?lat=51.21709661403662&lon=6.7782883744862374&apiKey={API_KEY}"

# headers = CaseInsensitiveDict()
# headers["Accept"] = "application/json"

# resp = requests.get(url, headers=headers, timeout=100)
# x = json.loads(resp.content)
# print(x['features'][0]['properties']['country'])
# print(resp.status_code)
