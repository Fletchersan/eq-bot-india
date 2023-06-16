from eq_api import QueryEarthquakeData
from reverse_geocode_api import Geocode_API
import json
from datetime import datetime
from dateutil import tz
class FilterAPIData:
    """
        filtered_earthquake_data -> [
            {
                'coordinates': {'lat': 33.0961, 'lon': 75.8961},
                'mag': 5,
                'place': '21 km NE of Bhadarwāh, India',
                'time': 'Tue Jun 13 19:03:40 2023'
            }, ...
        ]
    """
    FILTER_COUNTRY = 'INDIA'
    def __init__(self):
        # FIXME: UNDO
        self.earthquake_data = QueryEarthquakeData().query_earthquake_data('H')
        print(f"Length of earthquake events: {len(self.earthquake_data)}")
        self.earthquake_data_query = self._get_earthquake_data(self.earthquake_data)
        if len(self.earthquake_data) != 0:
            self.filtered_earthquake_data = self._filter_earthquake_data(self.earthquake_data_query)
        else:
            self.filtered_earthquake_data = []
    def _get_earthquake_data(self, raw_earthquake_data):
        earthquake_data_query = [
            x['geometry']['coordinates'] for x in raw_earthquake_data
        ]
        earthquake_data_query = [{'lon': x[0], 'lat': x[1]} for x in earthquake_data_query]
        print(earthquake_data_query[:5])
        return earthquake_data_query

    def _get_ist_time_from_time_in_ms(self, time_in_ms):
        from_tz = tz.gettz('UTC')
        to_tz = tz.gettz('Asia/Kolkata')

        return datetime.fromtimestamp(
            time_in_ms/1000
        ).replace(
            tzinfo=from_tz
        ).astimezone(to_tz).strftime('%c')

    def _filter_earthquake_data(self, earthquake_data_query):
        # FIXME: UNDO
        reverse_geocoded_data = Geocode_API(
            earthquake_data_query
        ).get_country_data()
        self.reverse_geocoded_data = reverse_geocoded_data
        filtered_queries = [
            query['query'] for query in reverse_geocoded_data 
            if query['country'].lower() == FilterAPIData.FILTER_COUNTRY.lower()
        ]
        # filtered_queries = earthquake_data_query
        filtered_earthquake_data = [
            {
                "mag": earthquake_event["properties"]["mag"],
                "place": earthquake_event["properties"]["place"],
                "time": self._get_ist_time_from_time_in_ms(
                    earthquake_event["properties"]["time"]
                ),
                "coordinates": {
                    'lon': earthquake_event['geometry']['coordinates'][0],
                    'lat': earthquake_event['geometry']['coordinates'][1]
                }
            } for earthquake_event in self.earthquake_data
            if {
                'lon': earthquake_event['geometry']['coordinates'][0],
                'lat': earthquake_event['geometry']['coordinates'][1]
            } in filtered_queries
        ]
        return filtered_earthquake_data
    
if __name__ == "__main__":
    filtered_data = FilterAPIData()
    from pprint import pprint
    pprint(filtered_data.filtered_earthquake_data[0])



