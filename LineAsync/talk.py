from LineFrugal.TalkService.ttypes import *

def loggedIn(fn):
    async def checkLogin(*args, **kwargs):
        if args[0].isLoggedIn:
            return await fn(*args, **kwargs)
        raise Exception("You have to loggedIn into LINE.")
    return checkLogin

class Talk(object):

    def __init__(self):
        self.isLoggedIn = True

    def setRevision(self, rev):
        self.revision = max(rev, self.revision)

    @loggedIn
    async def sendMessage(self, to: str, text: str, contentMetadata: dict = {}, contentType: int = 0) -> Message:
        msg = Message()
        msg.to = to
        msg.text, msg.contentMetadata, msg.contentType = text, contentMetadata, contentType
        try:
            await self.talk.call("sendMessage", -1, msg)
        except Exception as e:
            print(e)
