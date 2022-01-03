from twitchAPI.twitch import Twitch, AuthScope
from datetime import datetime
import threading
from enum import Enum
import pprint

class Requests(Enum):
    LAST_FOLLOWER = 1
    NUMBER_OF_FOLLOWERS = 2
    NUMBER_OF_VIEWERS = 3

class TwitchRequester:

    def __init__(self, userName: str) -> None:
        self.twitch = Twitch('o000ugumika3n9eakreixdlsuaui2f', '6qqe7r60nhieu60sac2oufjpf5vuu2', target_app_auth_scope=[AuthScope.USER_READ_FOLLOWS])
        self.id = self.twitch.get_users(logins=[userName])['data'][0]['id']
        # number of seconds between requests
        self.requestTimeouts = dict()
        self.requestTimeouts[Requests.LAST_FOLLOWER] = 10.0
        self.requestTimeouts[Requests.NUMBER_OF_FOLLOWERS] = 10.0
        self.requestTimeouts[Requests.NUMBER_OF_VIEWERS] = 1.0
        # last request time stamp
        self.requestTimestamps = dict()
        now = datetime.now()
        self.requestTimestamps[Requests.LAST_FOLLOWER] = now
        self.requestTimestamps[Requests.NUMBER_OF_FOLLOWERS] = now
        self.requestTimestamps[Requests.NUMBER_OF_VIEWERS] = now
        # protects class from multiple access
        self.lock = threading.Lock()
        # cache
        self.cache = dict()
        self.cache[Requests.LAST_FOLLOWER] = ""
        self.cache[Requests.NUMBER_OF_FOLLOWERS] = ""
        self.cache[Requests.NUMBER_OF_VIEWERS] = ""

        self.__forceAllRequests()

    
    def getLastFollower(self) -> str:
        return self.__getCacheEntry(Requests.LAST_FOLLOWER)

    def getNumberOfFollowers(self) -> str:
        return self.__getCacheEntry(Requests.NUMBER_OF_FOLLOWERS)

    def getNumberOfViewers(self) -> str:
        return self.__getCacheEntry(Requests.NUMBER_OF_VIEWERS)

    """Updates cache entry if necessary from api."""
    def __getCacheEntry(self, requestType: Requests) -> str:
        self.lock.acquire()

        timeout = self.requestTimeouts[requestType]
        secondsSinceLastRequest = (datetime.now() - self.requestTimestamps[requestType]).total_seconds()
        # if last request was too long ago -> request a new one
        if (secondsSinceLastRequest > timeout):
            # update
            self.__updateCacheEntry(requestType)
        response = self.cache[requestType]

        self.lock.release()
        return response


    def __updateCacheEntry(self, entry: Requests) -> None:
        if (entry == Requests.LAST_FOLLOWER or entry == Requests.NUMBER_OF_FOLLOWERS):
            self.__requestReadFollows()
        elif (entry == Requests.NUMBER_OF_VIEWERS):
            self.__requestStream()
        else:
            raise ValueError("Unknown request type: " + entry)

    def __requestReadFollows(self) -> None:
        # perform request
        followsResponse = self.twitch.get_users_follows(first=1, to_id=self.id)
        lastFollowerName = followsResponse['data'][0]['from_name']
        numberOfFollowers = followsResponse['total']
        # cache results
        self.cache[Requests.LAST_FOLLOWER] = lastFollowerName
        self.cache[Requests.NUMBER_OF_FOLLOWERS] = numberOfFollowers
        # save timestamp
        now = datetime.now()
        self.requestTimestamps[Requests.LAST_FOLLOWER] = now
        self.requestTimestamps[Requests.NUMBER_OF_FOLLOWERS] = now

    def __requestStream(self) -> None:
        response = self.twitch.get_streams(user_id=self.id)
        data = response['data']
        viewerCount = "0"
        if (data):
            # stream is online
            viewerCount = data[0]['viewer_count']
        # cache results
        self.cache[Requests.NUMBER_OF_VIEWERS] = viewerCount
        # save timestamp
        now = datetime.now()
        self.requestTimestamps[Requests.NUMBER_OF_VIEWERS] = now

    def __forceAllRequests(self) -> None:
        self.__requestReadFollows()
        self.__requestStream()