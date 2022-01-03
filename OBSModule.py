import os
import time
import threading

class OBSModule:
    """An OBSModule writes a string to a file for OBS to read."""

    def __init__(self, directoryPath: str, fileName: str, secondsBetweenUpdates: float, string: str = "n/a") -> None:
        self.file = directoryPath + os.path.sep + fileName
        self.string = string
        self.secondsBetweenUpdates = secondsBetweenUpdates
        self.stop = False
        self.thread = threading.Thread(target=self.threadFunction)

    """Write the string to the file."""
    def write(self):
        file = open(self.file, 'w')
        file.write(self.string)
        file.close()

    """Set new string."""
    def setString(self, newString: str):
        self.string = newString

    def getString(self) -> str:
        return self.string

    """Overwrite this to implement the thread functionality. This will be called repeatedly."""
    def threadWork(self) -> None:
        pass

    def threadFunction(self) -> None:
        
        while not self.stop:
            newString = self.threadWork()
            if (not self.getString() == newString):
                self.setString(newString)
                self.write()
            time.sleep(self.secondsBetweenUpdates)

    def runThread(self) -> None:
        self.thread.start()

    def stopThread(self) -> None:
        self.stop = True