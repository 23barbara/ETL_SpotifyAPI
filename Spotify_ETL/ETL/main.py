import ssl
import pandas as pd
import requests
import json
import datetime
from pymongo import MongoClient


USER_ID = "" # Spotify username - I've hidden mine in this published script due privacy concerns(read docs)

TOKEN = input("Enter token:") # spotify token can be generated here https://developer.spotify.com/console/get-recently-played/?limit=&after=&before=


if __name__ == "__main__":

    # - Extract part of the ETL process -

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    # Convert time to Unix timestamp in miliseconds
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs listened to in the last 24 hours
    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
        headers=headers)

    # store raw json data sent from API
    data = r.json()

    # - Transform part of the ETL Process -

    # select relevant fields from json object
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # store fields
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    data_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    # final result stored in a dataframe (good for debug or checking results)
    data_df = pd.DataFrame(data_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

    # - Load Stage of the ETL Process -

    # connection to MongoDB
    connection_string = "mongodb://localhost:27017/" # you can pass a URI or use localhost server

    client = MongoClient(connection_string)
    db = client["spotify_data"] # mongo database
    collection = db["songs"] # collection

    # insert result into collection
    collection.insert_one(data_dict)
