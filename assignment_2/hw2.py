import requests
import re
import matplotlib.pyplot as plt
import json
from assignment_2 import private_api_key


def lyrics_word_count_easy(artist, song, phrase):
    phrase_counter = 0
    try:
        response = requests.get("https://api.lyrics.ovh/v1/" + artist + "/" + song)
        json_text = json.loads(response.text)
        json_text = json_text.get('lyrics')
        for word in json_text.lower().split():
            if phrase in word:
                phrase_counter += 1
        return phrase_counter
    except AttributeError:
        return -1

def lyrics_word_count(artist, phrase):
    phrase_counter = 0
    response = requests.get("https://api.musixmatch.com/ws/1.1/artist.search?format=jsonp&callback=callback&q_artist=" + artist + "&apikey=" + private_api_key.ApiKey)
    response = str(response.text)[9:-2]
    artist_json = json.loads(response)
    artist_id = artist_json["message"]["body"]["artist_list"][0]["artist"]["artist_id"]
    album_list = []
    for page in range(0, 5):
        response2 = requests.get("https://api.musixmatch.com/ws/1.1/artist.albums.get?format=jsonp&callback=callback&artist_id=" + str(artist_id) + "&page_size=100" + "&page=" + str(page) + "&apikey=" + private_api_key.ApiKey)
        response2 = str(response2.text)[9:-2]
        albums_json = json.loads(response2)
        albums_songs = albums_json["message"]["body"]["album_list"]
        counter = 0
        for item in albums_songs:
            counter += 1
            print(counter)
            album_list.append(item["album"]["album_name"])
    album_list = set(album_list)
    return album_list


def visualize():
    pass


def main():
    print(lyrics_word_count_easy("Rick Astley", "Never Gonna Give You Up", "never"))
    print(lyrics_word_count("Taylor Swift", "yay"))

main()
