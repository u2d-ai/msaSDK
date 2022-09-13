# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Dict
import asyncio
from functools import lru_cache

if __name__ == '__main__':
    pass


class MSAUserProgress():

    def __init__(self) -> None:
        super().__init__()

        self.user_progress = {}

    async def addToProgress(self, event: str, message: Dict):  # user: str, progressPercent: int, progressMessage: str = ""
        data: Dict = message
        print(str(datetime.utcnow()), "addToProgress", data)
        if event and event.__eq__("user.progress"):
            if data:
                if "user" in data.keys():
                    user = data["user"]
                    progressPercent: int = 0
                    progressMessage: str = ""
                    if "pP" in data.keys():
                        progressPercent = data["pP"]
                    if "pM" in data.keys():
                        progressMessage = data["pM"]

                    msg: str = ""
                    utc_start: str = str(datetime.utcnow())
                    if len(progressMessage) > 0:
                        msg = utc_start + ": " + progressMessage
                    if user in self.user_progress.keys():
                        msgs: List = self.user_progress[user]
                        msgs.append({"data": progressPercent, "msg": msg})
                    else:
                        self.user_progress[user] = [{"data": progressPercent, "msg": msg}]
                    #print(user, msg, str(progressPercent))
                    await asyncio.sleep(0.1)

    def resetProgress(self, event: str, message: Dict):  # user: str
        data: Dict = message
        if event and event.__eq__("user.reset"):
            if data:
                if "user" in data.keys():
                    user = data["user"]
                    if user in self.user_progress.keys():
                        msgs: List = self.user_progress[user]
                        msgs.clear()
                        msgs.append({"data": 0, "msg": ""})


@lru_cache()
def getMSAUserProgress() -> MSAUserProgress:
    """
    This function returns a cached instance of the MSAUserProgress object.
    Note:
        Caching is used to prevent re-reading the environment every time the MSAUserProgress is used.
    """
    return MSAUserProgress()
