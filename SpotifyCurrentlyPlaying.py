from OBSModule import OBSModule
import time
import os
import urllib.request

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyCurrentlyPlaying(OBSModule):
    """Update Follower."""
    ALBUM_FILE_NAME = "Album.txt"
    SONG_FILE_NAME = "Song.txt"
    ARTWORK_FILE_NAME = "Artwork.jpg"
    ARTISTS_FILE_NAME = "Artists.txt"

    def __init__(self, directoryPath: str) -> None:
        # file name and seconds between updates unset
        super().__init__(directoryPath, "", 0)

        scope = "user-read-currently-playing"

        file = open("SpotifyClientId.txt", 'r')
        client_id = file.read()
        file.close()
        file = open("SpotifyClientSecret.txt", 'r')
        client_secret = file.read()
        file.close()
        print(client_id)
        print(client_secret)

        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=scope, 
                client_id=client_id, 
                client_secret=client_secret, 
                redirect_uri="http://localhost:8080")
                )

        self.albumFile = directoryPath + os.path.sep + self.ALBUM_FILE_NAME
        self.songFile = directoryPath + os.path.sep + self.SONG_FILE_NAME
        self.artworkFile = directoryPath + os.path.sep + self.ARTWORK_FILE_NAME
        self.artistsFile = directoryPath + os.path.sep + self.ARTISTS_FILE_NAME

        self.sleepTime = 30.0

    def writeToFile(self, fileName: str, stringToWrite: str) -> None:
        file = open(fileName, 'w')
        file.write(stringToWrite)
        file.close()

    def update(self) -> None:
        results = self.spotify.currently_playing()

        song = "Dead silence..."
        album = ""
        artists = ""
        artwork = ""

        if results["is_playing"]:
            item = results["item"]

            # get artist names and stuff them in one string
            artistsRaw = item["artists"]
            numberOfArtists = len(artistsRaw)
            for index in range(numberOfArtists):
                if index == numberOfArtists - 1:
                    artists += artistsRaw[index]["name"]
                else:
                    artists += artistsRaw[index]["name"]
                    aritsts += ", "

            # get album name and image
            albumRaw = item["album"]
            album = albumRaw["name"]
            artwork = albumRaw["images"][0]["url"]
            
            # get song name
            song = item["name"]

            # sleep time computed from duration and progress
            # (this is not 100% accurate but good enough)
            self.sleepTime = (item["duration_ms"] - results["progress_ms"]) / 1000.0

        
        # now write them all to files
        self.writeToFile(self.songFile, song)
        self.writeToFile(self.albumFile, album)
        self.writeToFile(self.artistsFile, artists)
        urllib.request.urlretrieve(artwork, self.artworkFile)


    """Special behaviour of thread function because we have multiple strings."""
    def threadFunction(self) -> None:
        while not self.stop:
            # do a single request which also write to files
            self.update()
            time.sleep(self.sleepTime)