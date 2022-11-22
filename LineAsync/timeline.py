# -*- coding: utf -*-
from .channel import Channel
import time, json, random, traceback, livejson

class Timeline(Channel):

    def __init__(self):
        Channel.__init__(self)
        self.server.setTimelineHeadersWithDict({
            "x-lsr": "JP",
            "X-Line-ChannelToken": "",
            "X-Line-Application": self.server.APP_NAME,
            "Content-Type": "application/json; charset=UTF-8",
            "x-lal": "en_GB",
            "x-line-global-config": "discover.enable=false; follow.enable=true; reboot.phase=none",
            "x-line-bdbtemplateversion": "v1",
            "user-agent": self.server.USER_AGENT,
            "x-line-mid": self.profile.mid,
            "accept-encoding": "gzip",
            "x-lpv": "1",
        })

    async def updateProfileCover(self, homeId = None, coverObjectId = None, videoCoverObjectId = None, storyShare = True):
        data = {
            "homeId": self.profile.mid if not homeId else homeId,
            "coverObjectId": coverObjectId,
            "storyShare": storyShare
        }
        if videoCoverObjectId:
            data.update({
                "videoCoverObjectId": videoCoverObjectId
            })
        headers = self.server.additionalHeaders(self.server.timelineHeaders, {"X-Line-ChannelToken": await self.loginChannel('HOME')})
        r = await self.server.request("POST", self.server.LINE_GWS_SERVER_HOST + "/hm/api/v1/home/cover.json", 'text', content = json.dumps(data), headers = headers)
        if r.status_code == 200:
            if homeId == self.profile.mid:
                return await self.postCoverToTimeline(coverObjectId, videoCoverObjectId)
            return True

    async def postCoverToTimeline(self, coverObjectId, videoCoverObjectId = None):
        data = {
            "coverObjectId": coverObjectId
        }
        if videoCoverObjectId:
            data.update({"videoCoverObjectId": videoCoverObjectId})
        channelToken = await self.loginChannel('HOME')
        headers = self.server.additionalHeaders(self.server.timelineHeaders, {"X-Line-ChannelToken": channelToken})
        r = await self.server.request("POST", self.server.LINE_GWS_SERVER_HOST + "/mh/api/v1/home/post/cover.json", 'text', content = json.dumps(data), headers = headers)
        return r.json()

    async def getHomeProfile(self, homeId = None, styleMediaVersion = 'v2', timelineVersion = 'v57', storyVersion = 'v8', profileBannerRevision = 0):
        params = {
            "homeId": homeId if homeId else self.profile.mid,
            "styleMediaVersion": styleMediaVersion,
            "timelineVersion": timelineVersion,
            "storyVersion": storyVersion,
            "profileBannerRevision": profileBannerRevision
        }
        if params.get("homeId").startswith("c"):
            path = "/hm/api/v1/home/groupprofile.json"
        else:
            path = "/hm/api/v1/home/profile.json"
        headers = self.server.additionalHeaders(self.server.timelineHeaders, {"X-Line-ChannelToken": await self.loginChannel('HOME')})
        r = await self.server.request("GET", self.server.LINE_GWS_SERVER_HOST + path, params = params, headers = headers)
        return r.json()

    async def createPost(self, homeId: str, text: str = None, sharedPostId: str = None, textSizeMode: str = "NORMAL",
                   backgroundColor: str = "#FFFFFF", textAnimation: str = "NONE", readPermissionType: str = "ALL",
                   readPermissionGids: list = None, holdingTime: int = None, stickerIds: list = None,
                   stickerPackageIds: list = None, locationLatitudes: list = None, locationLongitudes: list = None,
                   locationNames: list = None, mediaObjectIds: list = None, mediaObjectTypes: list = None, medias = [],
                   sourceType: str = "TIMELINE"):
        """
        - readPermissionType:
            ALL,
            FRIEND,
            GROUP,
            EVENT,
            NONE;
        - textSizeMode:
            AUTO,
            NORMAL;
        - textAnimation:
            NONE,
            SLIDE,
            ZOOM,
            BUZZ,
            BOUNCE,
            BLINK;
        """
        params = {
            'homeId': homeId,
            'sourceType': sourceType
        }
        postInfo = {
            "readPermission": {
                "type": readPermissionType,
                "gids": readPermissionGids
            },
        }
        stickers = []
        locations = []
        medias = medias
        """for stickerIndex, stickerId in enumerate(stickerIds):
            stickers.append({
                "id": stickerId,
                "packageId": stickerPackageIds[stickerIndex],
                "packageVersion": 1,
                "hasAnimation": True,  # TODO: check it
                "hasSound": True,  # TODO: check it
                "stickerResourceType": "ANIMATION"  # TODO: check it
            })
        for locatioIndex, locationLatitude in enumerate(locationLatitudes):
            locations.append({
                "latitude": locationLatitude,
                "longitude": locationLongitudes[locatioIndex],
                "name": locationNames[locatioIndex]
            })"""
        contents = {
            "contentsStyle": {
                "textStyle": {
                    "textSizeMode": textSizeMode,
                    "backgroundColor": backgroundColor,
                    "textAnimation": textAnimation
                },
                "mediaStyle": {
                    "displayType": "GRID_1_A"
                },
            },
            "stickers": stickers,
            "locations": locations,
            "media": medias
        }
        if holdingTime is not None:
            postInfo["holdingTime"] = holdingTime
        if text is not None:
            contents['text'] = text
        if sharedPostId is not None:
            contents['sharedPostId'] = sharedPostId
        data = {
            "postInfo": postInfo,
            "contents": contents
        }
        headers = self.server.additionalHeaders(self.server.timelineHeaders, {"X-Line-ChannelToken": await self.loginChannel('HOME')})
        r = await self.server.request("POST", self.server.LINE_GWS_SERVER_HOST + "/mh/api/v57/post/create.json", "text", params = params, content = json.dumps(data), headers = headers)
        return r.json()

    """ Login Channel """
    async def loginChannel(self, channelType, updated = False):
        if "channelToken" in self.settings.data:
            if round(time.time() - self.settings["channelToken"]["time"]) >= 604800:
                channelToken = await self.approveChannelAndIssueChannelToken(
                    self.server.CHANNEL_ID[f'LINE_{channelType}']
                ).channelAccessToken
                self.settings["channelToken"].update({
                    "time": time.time(),
                    "channelToken": channelToken
                })
                self.channelToken = channelToken
                return channelToken
            return self.settings["channelToken"]["channelToken"]
        channel  = await self.approveChannelAndIssueChannelToken(
            self.server.CHANNEL_ID[f'LINE_{channelType}']
        )
        self.settings["channelToken"] = {"time": time.time(), "channelToken": channel.channelAccessToken}
        self.channelToken = channel.channelAccessToken
        return channel.channelAccessToken