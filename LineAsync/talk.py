from LineFrugal.ttypes import *
import livejson, asyncio
from unidecode import unidecode

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
    async def getProfile(self):
        self.profile = await self.talk.call("getProfile", 4)
        return self.profile

    @loggedIn
    async def sendMessage(self, to: str, text: str, contentMetadata: dict = {}, contentType: int = 0) -> Message:
        msg = Message()
        msg.to = to
        msg.text, msg.contentMetadata, msg.contentType = text, contentMetadata, contentType
        try:
            await self.talk.call("sendMessage", -1, msg)
        except Exception as e:
            print(e)

    """ Chat """
    @loggedIn
    async def getAllChatMids(self, withMembers = True, withInvitees = True):
        return await self.talk.call('getAllChatMids', GetAllChatMidsRequest(withMembers, withInvitees), 4)

    @loggedIn
    async def getGroupIdsJoined(self):
        chatList = await self.getAllChatMids(True, False)
        chatIds = list(chatList.memberChatMids)
        chats = []
        for i in range(0, len(chatIds), 100):
            chatMids = []
            for no, chatId in enumerate(chatIds[i:i+100], i+1):
                chatMids.append(chatId)
            chatss = await self.getChats(*chatMids, withMembers = True, withInvitees = True)
            chats += chatss.chats
            chatMids = []
        chats = sorted(chats, key = lambda chat: unidecode(chat.chatName.lower()))
        self.groupList = chats
        self.groupListIds = [chat.chatMid for chat in chats]
        return chats

    @loggedIn
    async def getChats(self, *chatIds, withMembers = False, withInvitees = False):
        req = GetChatsRequest(
            [*chatIds], withMembers, withInvitees
        )
        return await self.talk.call('getChats', req, 4)

    """ E2EE """
    @loggedIn
    async def getE2EEPublicKeys(self):
        return await self.talk.call('getE2EEPublicKeys')

    @loggedIn
    async def getLastE2EEPublicKeys(self, chatMid, toType = "GROUP"):
        return await self.talk.call('getLastE2EEPublicKeys', chatMid)

    @loggedIn
    async def getLastE2EEGroupSharedKey(self, chatMid):
        return await self.talk.call('getLastE2EEGroupSharedKey', 2, chatMid)

    @loggedIn
    async def negotiateE2EEPublicKey(self, mid):
        return await self.talk.call('negotiateE2EEPublicKey', mid)