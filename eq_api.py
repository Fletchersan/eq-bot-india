"""Queries for earthquake data"""
import json
from datetime import datetime, timedelta
from typing import List

import requests

class QueryEarthquakeData:
    MINIMUM_MAGNITUDUE = 5
    FORMAT = 'geojson'
    URL_ROOT = "https://earthquake.usgs.gov/fdsnws/event/1"
    QUERY_TIME_STRING_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    
    def __init__(self):
        self.current_time: datetime = datetime.now()
    
    def _get_query_for_earthquakes_in_the_last_hour(self):
        """Queries all earthquake data for minimum scale starting from time of
        object creation"""
        minmagnitude = f"minmagnitude={QueryEarthquakeData.MINIMUM_MAGNITUDUE}"
        query_time_string_format = QueryEarthquakeData().QUERY_TIME_STRING_FORMAT
        end_time: str = self.current_time.strftime(query_time_string_format)
        start_time: str = (self.current_time - timedelta(hours=1)).strftime(
            QueryEarthquakeData.QUERY_TIME_STRING_FORMAT
        )
        format_clause: str= f"format={QueryEarthquakeData.FORMAT}"
        time_window: str = f"starttime={start_time}&endtime={end_time}"
        query_string: str = f"query?{format_clause}&{time_window}&{minmagnitude}"
        request_url: str = f"{QueryEarthquakeData.URL_ROOT}/{query_string}"
        return request_url

    def query_earthquake_data(self, interval: str = 'H') -> List:
        '''Returns data in the form of a list where each element is of the type
    [{
      "type": "Feature",
      "properties": {
        "mag": 6.5,
        "place": "32 km W of Sola, Vanuatu",
        "time": 1388592209000,
        "updated": 1651596180609,
        "tz": null,
        "url": "https://earthquake.usgs.gov/earthquakes/eventpage/usc000lvb5",
        "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=usc000lvb5&format=geojson",
        "felt": null,
        "cdi": null,
        "mmi": 4.262,
        "alert": "green",
        "status": "reviewed",
        "tsunami": 1,
        "sig": 650,
        "net": "us",
        "code": "c000lvb5",
        "ids": ",pt14001000,at00myqcls,usc000lvb5,iscgem604060577,",
        "sources": ",pt,at,us,iscgem,",
        "types": ",cap,impact-link,losspager,moment-tensor,origin,phase-data,shakemap,",
        "nst": null,
        "dmin": 3.997,
        "rms": 0.76,
        "gap": 14,
        "magType": "mww",
        "type": "earthquake",
        "title": "M 6.5 - 32 km W of Sola, Vanuatu"
      },
      "geometry": { "type": "Point", "coordinates": [167.249, -13.8633, 187] },
      "id": "usc000lvb5"
    },...]        
        '''
        time_delta_to_query = {
            "H": self._get_query_for_earthquakes_in_the_last_hour
        }
        request_url = time_delta_to_query[interval]()
        response = requests.request('GET', request_url, timeout=100)
        status_code = response.status_code
        if status_code == 200:
            print("status code fine")
            content = json.loads(response.content)
            earthquakes = content['features']
            return earthquakes
        return []

if __name__ == "__main__":
    earthquake_data_in_last_hour = QueryEarthquakeData().query_earthquake_data('H')
    import pickle
    with open('eq_data.pkl', 'wb') as f:
        pickle.dump(earthquake_data_in_last_hour, f)

