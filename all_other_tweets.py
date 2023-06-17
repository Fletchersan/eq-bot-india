import json
import os
import traceback
from ast import literal_eval
from datetime import datetime

from dotenv import load_dotenv, set_key

import main
from utils.get_earthquake_data import FilterAPIData

try:
    print(f"INFO: TIME OF RUN -> {datetime.now().strftime('%c')}")
    load_dotenv('.env')
    data = literal_eval(
        json.loads(os.getenv('TOKEN').replace('\\',''))
    )
    twitter = main.make_token()
    client_id = os.environ.get("TWITTER_CLIENT_ID")
    client_secret = os.environ.get("TWITTER_CLIENT_SECRET")
    TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
    print('getting refresh token')
    refreshed_token = twitter.refresh_token(
        client_id=client_id,
        client_secret=client_secret,
        token_url=TOKEN_URL,
        refresh_token=data["refresh_token"],
    )
    print("obtained refresh token")
    st_refreshed_token = f'"{refreshed_token}"'

    set_key('.env', 'TOKEN', st_refreshed_token)

    earthquakes_in_india = FilterAPIData().filtered_earthquake_data

    for earthquake in earthquakes_in_india:
        payload_content = f"""Richter {earthquake['mag']} Earthquake!!\nWhere: {earthquake['place']}\nWhen: {earthquake['time']}\n#earthquake_alert"""
        payload = {"text": payload_content}
        main.post_tweet(payload, refreshed_token)

except Exception as E:
    print(f"Error: \n {E.__repr__()}")
    traceback.print_exc()
finally:
    print("******************************")