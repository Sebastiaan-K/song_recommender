import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from time import sleep


client_credentials_manager = SpotifyClientCredentials(client_id="c66d5a293cea48a2b218269ce954e9b5", client_secret="99c7012918c74c9dbafa4accd8f21d5b")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# function to search for songs
def search_song(title, artist, limit=5):
    query = "tracks: "+title+" artist: "+artist
    try:
        result = sp.search(query, limit=limit)
        song_id = result['tracks']['items'][0]['id']
        return song_id
    except:
        return "not found"
        
def get_audio_features(list_of_song_ids):
    """Collects audio features for a list of song IDs.
    Input:
    list_of_song_ids: A list of song IDs.
    Returns:
    pandas DataFrame containing the audio features for the IDs.
    """
    # split the list of song IDs into chunks of 50 to avoid hitting the rate limit.
    chunks = [list_of_song_ids[i:i + 50] for i in range(0, len(list_of_song_ids), 50)]
    # get audio features
    all_features = []
    for chunk in chunks:
        sleep(5)  
        features_chunk = sp.audio_features(chunk)
        if features_chunk is not None:  # check if the result is not None.
            valid_features = [f for f in features_chunk if f is not None]
            all_features.extend(valid_features)
        else:
            print("Failed to fetch features for chunk:", chunk)
    # convert the list of dictionaries to df
    df_audio_features = pd.DataFrame(all_features)
    return df_audio_features
    
def add_audio_features(df1, df2, merge_on, drop_duplicates_on):
    # Merge dataframes
    merged_df = pd.merge(df1, df2, left_on=merge_on, right_on='id', how='left')
    # Drop duplicates
    merged_df.drop_duplicates(subset=drop_duplicates_on, inplace=True)
    # Reset index
    merged_df.reset_index(drop=True, inplace=True)
    return merged_df
