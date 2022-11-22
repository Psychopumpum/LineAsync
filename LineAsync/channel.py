


class Channel(object):

    def __init__(self):
        pass

    async def approveChannelAndIssueChannelToken(self, channelId):
        return await self.channel.call('approveChannelAndIssueChannelToken', channelId)

    async def issueChannelToken(self, channelId):
        return await self.channel.call('issueChannelToken', channelId)