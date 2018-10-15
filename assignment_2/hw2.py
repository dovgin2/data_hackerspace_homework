import requests
import re
import numpy as np
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
    total_phrase_counter = 0
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
        for item in albums_songs:
            album_list.append(item["album"]["album_id"])
    album_list = set(album_list)
    album_list = list(album_list)
    track_name_list = []
    for id in album_list:
        response3 = requests.get("https://api.musixmatch.com/ws/1.1/album.tracks.get?format=jsonp&callback=callback&album_id=" + str(id) + "&apikey=" + private_api_key.ApiKey)
        response3 = str(response3.text)[9:-2]
        tracks_json = json.loads(response3)
        track_songs = tracks_json["message"]["body"]["track_list"]
        for item in track_songs:
            track_name_list.append(item["track"]["track_name"])
    track_name_list = set(track_name_list)
    track_name_list = list(track_name_list)
    for track_name in track_name_list:
        try:
            num_to_add = lyrics_word_count_easy(artist, track_name, phrase)
        except json.decoder.JSONDecodeError:
            num_to_add = 0
        if num_to_add != -1:
            total_phrase_counter += num_to_add
    return total_phrase_counter


def visualize():
    x = np.array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12., 13., 14., 15., 16., 17., 18., 19., 20., 21., 22., 23., 24., 25., 26., 27., 28., 29.])
    y = np.array([0., 25., 27., 4., -22., -28., -8., 19., 29., 12., -16., -29., -16., 12., 29., 19., -8., -28., -22., 4., 27., 25., -0., -25., -27., -3., 22., 28., 8., -19.])
    f, axarr = plt.subplots(2, 2)
    axarr[0, 0].plot(x, y)
    axarr[0, 0].set_title('Line Graph')
    axarr[0, 1].scatter(x, y)
    axarr[0, 1].set_title('Scatter')
    axarr[1, 0].hist(x, bins=[0, 5, 10, 15, 20])
    axarr[1, 0].set_title('x Histogram')
    axarr[1, 1].hist(y, bins=[-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20])
    axarr[1, 1].set_title('y Histogram')
    for ax in axarr.flat:
        ax.set(xlabel='x-label', ylabel='y-label')
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axarr.flat:
        ax.label_outer()
    plt.show()


def main():
    #print(lyrics_word_count_easy("Rick Astley", "Never Gonna Give You Up", "never"))
    #print(lyrics_word_count("Taylor Swift", "you"))
    visualize()

main()
