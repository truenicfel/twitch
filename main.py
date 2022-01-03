from LastFollower import LastFollower
from Stats import Stats
from TwitchRequester import TwitchRequester

twitchRequester = TwitchRequester("tolkinlol")

lastFollower = LastFollower("E:\Dokumente\OBSModules", twitchRequester)
lastFollower.runThread()

stats = Stats("E:\Dokumente\OBSModules", twitchRequester)
stats.runThread()

input("Press Enter to stop!")

lastFollower.stopThread()
stats.stopThread()
print("Stopping... This might take a few seconds...")