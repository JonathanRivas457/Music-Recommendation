# Overview
The goal of this project is to build a music recommendation system that:

1. Extracts audio features from songs by converting them to spectrograms.
2. Groups similar songs using deep clustering.
3. Recommends songs by matching them to clusters that share similar features.

# Extractor
The Extractor component of the system fetches artist tracks and prepares them for clustering by following these steps:

1. Spotify API:
   Use the Spotify API to get the top tracks of an artist.

2. Web Scraping:
   Use Selenium to scrape YouTube URLs for the retrieved tracks.

3. Download Songs:
   Use yt-dlp (a powerful tool for downloading videos from YouTube) to download the songs in audio format.

4. Extract Spectrograms:
   Use Librosa to load the audio files and convert them into spectrograms, which are then used as input for deep learning models.

# Deep Clustering
The Deep Clustering part of the project groups the songs into clusters based on their audio features and learns from these clusters using deep learning techniques:

1. Feature Extraction with CNN:
   A Convolutional Neural Network (CNN) is used to extract high-level features from the spectrogram images.

2. Clustering with K-means:
   K-means clustering is applied to the features extracted by the CNN, creating pseudo-labels for the songs based on their similarity.

3. Classifying with CNN:
   A classification model is trained on the spectrograms and their corresponding pseudo-labels to refine the feature learning process.

4. Final Clusters:
   After training, the final clusters represent groups of similar songs. The final CNN layer is used to generate feature vectors for each spectrogram, and songs are assigned to clusters based on         these vectors.

