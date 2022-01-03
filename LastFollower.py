from OBSModule import OBSModule
from TwitchRequester import TwitchRequester
import threading
import time

class LastFollower(OBSModule):
    """Update Follower."""
    FILE_NAME = "LastFollower.txt"

    def __init__(self, directoryPath: str, twitchRequester: TwitchRequester) -> None:
        super().__init__(directoryPath, self.FILE_NAME, 10)
        self.twitchRequester = twitchRequester


    """Request the last follower once and return the name as a string."""
    def threadWork(self) -> str:
        return self.twitchRequester.getLastFollower()


