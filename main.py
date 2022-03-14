from LastFollower import LastFollower
from Stats import Stats
from TwitchRequester import TwitchRequester
from SpotifyCurrentlyPlaying import SpotifyCurrentlyPlaying

twitchRequester = TwitchRequester("nicfel")

path = "E:\Dokumente\OBSModules"

lastFollower = LastFollower(path, twitchRequester)
lastFollower.runThread()

stats = Stats(path, twitchRequester)
stats.runThread()

spotify = SpotifyCurrentlyPlaying(path)
spotify.runThread()

input("Press Enter to stop!")

# lastFollower.stopThread()
# stats.stopThread()

spotify.stopThread()

print("Stopping... This might take a few seconds...")