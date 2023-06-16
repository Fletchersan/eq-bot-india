import main
import json
import os
from dotenv import get_key, load_dotenv, set_key
from ast import literal_eval
from get_earthquake_data import FilterAPIData
from datetime import datetime
print(f"INFO: TIME OF RUN -> {datetime.now().strftime('%c')}")
load_dotenv('.env')
data = literal_eval(
    os.getenv('TOKEN').replace('\\','')
)
print(data)
twitter = main.make_token()
client_id = os.environ.get("TWITTER_CLIENT_ID")
client_secret = os.environ.get("TWITTER_CLIENT_SECRET")
token_url = "https://api.twitter.com/2/oauth2/token"
print('getting refresh token')
refreshed_token = twitter.refresh_token(
    client_id=client_id,
    client_secret=client_secret,
    token_url=token_url,
    refresh_token=data["refresh_token"],
)
print("obtained refresh token")
st_refreshed_token = '"{}"'.format(refreshed_token)
j_refreshed_token = json.loads(st_refreshed_token)

set_key('.env', 'TOKEN', j_refreshed_token)

earthquakes_in_india = FilterAPIData().filtered_earthquake_data

for earthquake in earthquakes_in_india:
    payload_content = f"""Richter {earthquake['mag']} Earthquake!!\nWhere: {earthquake['place']}\nWhen: {earthquake['time']}\n#earthquake_alert"""
    payload = {"text": payload_content}
    main.post_tweet(payload, refreshed_token)
