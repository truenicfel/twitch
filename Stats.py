from OBSModule import OBSModule
from TwitchRequester import TwitchRequester
import os

class Stats(OBSModule):
    """Update Follower."""
    STATS_FILE_NAME = "Stats.txt"
    FOLLOWER_COUNT_FILE_NAME = "FollowerCount.txt"

    def __init__(self, directoryPath: str, twitchRequester: TwitchRequester) -> None:
        super().__init__(directoryPath, self.STATS_FILE_NAME, 10)
        self.twitchRequester = twitchRequester
        self.followerCountFilePath = directoryPath + os.path.sep + self.FOLLOWER_COUNT_FILE_NAME
        # average viewer count
        self.averageViewers =  int(self.twitchRequester.getNumberOfViewers())
        self.alpha = 0.01

        # last time followers
        file = open(self.followerCountFilePath)
        self.previousStreamFollowerCount = int(file.read())
        file.close()


    """Request the last follower once and return the name as a string."""
    def threadWork(self) -> str:
        followerCount = int(self.twitchRequester.getNumberOfFollowers())
        file = open(self.followerCountFilePath, 'w')
        file.write(str(followerCount))
        file.close()
        newFollowers = followerCount  - self.previousStreamFollowerCount

        viewerCount = int(self.twitchRequester.getNumberOfViewers())
        self.averageViewers = (self.alpha * viewerCount) + (1.0 - self.alpha) * self.averageViewers

        result = ""
        result += "Total Followers: " + str(followerCount) + "   "
        result += "New Followers: " + str(newFollowers) + "   "
        result += "Current Viewers: " + str(viewerCount) + "   "
        result += "Average Viewers: " + "{:.2f}".format(self.averageViewers) + "   "

        return result



