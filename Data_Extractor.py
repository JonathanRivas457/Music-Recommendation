import yt_dlp
import ffmpeg
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm
import time
import json
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
import numpy as np
import argparse

def get_artist_tracks(artists):

    # Dictionary to store songs
    song_dictionary = {}

    # Initialize the Spotify client
    client_credentials_manager = SpotifyClientCredentials(client_id='98c92df339b44755b057c9e2be8a9d24', client_secret='295fb3083f4d4e348acf8afded757d9a')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get top tracks
    for artist_id in tqdm(artists, desc="Getting Artist Tracks", unit="artists"):
        artist = sp.artist(artist_id)
        top_tracks = sp.artist_top_tracks(artist_id, country='US')
        for track in top_tracks['tracks']:
            key = artist['name'] + "-" + track['name']
            song_dictionary[key] = 'temp'


    return song_dictionary

def get_song_urls(song_dictionary):

    # Setup driver
    driver = webdriver.Firefox()

    # Go through each query
    for song, link in tqdm(song_dictionary.items(), desc="Getting Track URLs", unit="song"):
        
        # Get URL
        url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
        driver.get(url)
        sleep(20)
        # Retrieve the page source (HTML content)
        html_content = driver.page_source

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all <a> tags
        curr_link = ""
        for video in soup.find_all('a', href=True):
            if "/watch?v=" in video['href']:

                # Get value of the first link and break
                full_link = f"https://www.youtube.com{video['href']}"
                curr_link = full_link
                break

        song_dictionary[song] = curr_link
    driver.quit()
    return song_dictionary


def download_audios(song_dictionary):
    for song, url in tqdm(song_dictionary.items(), desc="Downloading Audios", unit="songs"):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{song}.%(ext)s',
                'socket_timeout': 120,
                'retries': 5,
                'retry_sleep': 30,
                'quiet': True,
                'no_range': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except yt_dlp.utils.DownloadError as e:
            print(f"Attempt failed: {e}")

        ffmpeg_location = "C:/ffmpeg/ffmpeg-2024-03-04-git-e30369bc1c-full_build/ffmpeg-2024-03-04-git-e30369bc1c-full_build/bin/ffmpeg.exe"
        input_file = f"{song}.webm"
        output_file = f"RNBwavAudios/{song}.wav"
        ffmpeg.input(input_file).output(output_file).run(cmd=ffmpeg_location, capture_stdout=True, capture_stderr=True)

        get_spectrogram(output_file, song)


def get_spectrogram(audio_path, song_name) :
    y, sr = librosa.load(audio_path)

    # Create spectrogram
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

    resolutions = [[200, 100], [300, 200], [500, 300], [2000, 1500]]
    for res in resolutions:
        res1 = res[0]
        res2 = res[1]
        output_dir = f"RNBSpectrograms_{res1}x{res2}"
        os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
        output_path = f"{output_dir}/{song_name}_{res1}x{res2}.png"
        plt.figure(figsize=(res1/100, res2/100))
        librosa.display.specshow(spectrogram_db, sr=sr, x_axis='time', y_axis='mel')
         
        plt.savefig(output_path)
        plt.close()


song_dictionary = get_artist_tracks(['7tYKF4w9nC0nq9CsPZTHyP'])
song_dictionary = get_song_urls(song_dictionary)

download_audios(song_dictionary)
