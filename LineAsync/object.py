#!usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib, time, json, random
from typing import Union
import base64


class Object(object):

    async def updateProfilePicture(self, path, type = "p", uploadToStory = True):
        files = {'file': open(path, 'rb')}
        params = {'oid': self.profile.mid, 'type': 'image'}
        if type == 'vp':params.update({'ver': '2.0', 'cat': 'vp.mp4'})
        headers = self.server.talkHeaders
        if uploadToStory:
            headers.update({"x-talk-meta": "eyJwcm9maWxlQ29udGV4dCI6eyJzdG9yeVNoYXJlIjp0cnVlfX0="})
        data = {"params": self.genOBSParams(params)}
        r = await self.server.request("POST", self.server.OBJECT_STORAGE_SERVER_HOST + "/talk/p/upload.nhn", 'text', data = data, headers = headers, files = files)
        self.removeFile(path)
        if r.status_code != 201:
            raise Exception("Update Profile Picture failure.")
        return True

    async def updateVideoAndPictureProfile(self, path_p, path, uploadToStory = True):
        files = {"file": open(path, "rb")}
        data  = {
            "params": self.genOBSParams({
                "oid": self.profile.mid,
                "cat": "vp.mp4",
                "type": "video",
                "ver": "2.0"
            })
        }
        headers = self.server.talkHeaders
        if uploadToStory:headers.update({"x-talk-meta": "eyJwcm9maWxlQ29udGV4dCI6eyJzdG9yeVNoYXJlIjp0cnVlfX0="})
        r = await self.server.request("POST", self.server.OBJECT_STORAGE_SERVER_HOST + '/talk/vp/upload.nhn', 'text', data = data, files = files, headers = headers)
        self.removeFile(path)
        if r.status_code == 200:
            raise Exception("Update video profile failure.")
        return await self.updateProfilePicture(path_p, "vp")

    async def updateGroupPicture(self, groupId, path):
        files = {'file': open(path, 'rb')}
        data = {'params': self.genOBSParams({'oid': groupId, 'type': 'image'})}
        headers = self.server.talkHeaders
        headers.update({'x-obs-params': self.genOBSParams({'name': path, 'type': 'image', 'ver':'2.0'}, 'b64')})
        r = await self.server.request('POST', self.server.OBJECT_STORAGE_SERVER_HOST + '/talk/g/upload.nhn', 'text', headers=headers, data=data, files=files)
        self.removeFile(path)

    """ Uploaders """
    async def uploadObjTalk(self, path, type = "image", returnAs = "objId", objId = None, to = None, talkMeta = None, duration = None, remove = True):
        if returnAs not in ["objId", "bool", "headers"]:
            raise Exception("Invalid returnAs value")
        if type not in ["image", "gif", "video", "audio", "file"]:
            raise Exception("Invalid type value")
        headers = self.server.talkHeaders
        files = {
            "file": open(path, "rb")
        }
        host_url = self.server.OBJECT_STORAGE_SERVER_HOST
        if type == "image" or type == "video" or type == "audio" or type == "file":
            if talkMeta:
                path_url = "/r/talk/m/reqseq"
                data = {
                    "params": self.genOBSParams({
                        "oid": "reqseq",
                        "type": type,
                        "tomid": to,
                        "ver": "2.0",
                        "name": files['file'].name,
                        "reqseq": str(int(time.time()))
                    })
                }
            else:
                path_url = "/talk/m/upload.nhn"
                data = {
                    'params': self.genOBSParams({
                        'type': type,
                        'ver': '2.0',
                        'name': files['file'].name,
                        'oid': objId
                    })
                }
        elif type == "gif":
            path_url = "/r/talk/m/reqseq"
            files = None
            data = open(path, "rb").read()
            params = {
                "name": "%s" % str(time.time() * 1000),
                "oid": f'{objId}',
                "reqseq": "%s" % str(self.revision),
                "tomid": "%s" % str(to),
                "cat": "original",
                "type": "image",
                "ver": "1.0",
            }
            headers = self.server.additionalHeaders(self.server.talkHeaders, {
                "Content-Type": "image/gif",
                "Content-Length": str(len(data)),
                "x-obs-params": self.genOBSParams(params, "b64"),
            })
        if talkMeta:
            headers.update({
                "x-talk-meta": talkMeta
            })
        r = await self.server.request('POST', host_url + path_url, 'text', data=data, headers=headers, files=files)
        if r.status_code != 201:
            raise Exception("Upload %s failure." % type)
        if remove:self.removeFile(path)
        if returnAs == "objId":
            return r.headers.get('x-obs-oid')
        elif returnAs == "bool":
            return True
        else:
            return r.get('headers')

    async def uploadMultiImage(self, path, to):
        sqrd_base = [13, 0, 18, 11, 11]
        hashmap = {
            "GID" : "0",
            "GSEQ": "1",
            "GTOTAL": str(len(path))
        }
        sqrd = sqrd_base + self.getIntBytes(len(hashmap.keys()))
        for hm in hashmap.keys():
            sqrd += self.getStringBytes(hm)
            sqrd += self.getStringBytes(hashmap[hm])
        sqrd += [0]
        data = bytes(sqrd)
        msg = json.dumps({
            "message": base64.b64encode(data).decode('utf-8')
        })
        talkMeta = base64.b64encode(msg.encode('utf-8')).decode('utf-8')
        result = await self.uploadObjTalk(path[0], 'image', to=to, talkMeta=talkMeta, returnAs = "headers")
        groupMessageId = result['x-line-message-gid']
        messageId = [result['x-obs-oid']]
        hashmap.update({'GID': groupMessageId})
        no = 1
        self.removeFile(path[0])
        for path in path[1:]:
            no += 1
            hashmap.update({'GSEQ': str(no)})
            sqrd = sqrd_base + self.getIntBytes(len(hashmap.keys()))
            for hm in hashmap.keys():
                sqrd += self.getStringBytes(hm)
                sqrd += self.getStringBytes(hashmap[hm])
            sqrd += [0]
            data = bytes(sqrd)
            msg = json.dumps({
                "message": base64.b64encode(data).decode('utf-8')
            })
            talkMeta = base64.b64encode(msg.encode('utf-8')).decode('utf-8')
            time.sleep(1)
            res = await self.uploadObjTalk(path, 'image', to=to, talkMeta=talkMeta, returnAs = "headers")
            self.removeFile(path)
            messageId.append(res['x-obs-oid'])
        return messageId

    """ Home """
    async def uploadObjectHome(self, path, type = "image", objId = None, returnAs = "headers", **kwargs):
        if returnAs not in ["headers", "objId", "bool"]:
            raise Exception("Invalid returnAs value")
        if type not in ["image", "video", "gif"]:
            raise Exception("Invalid type value")
        files = {"file": open(path, "rb")}
        if not objId:
            objId = hashlib.md5(f'Psychopumpum_{str(time.time()*1000)}'.encode()).hexdigest()
        data = open(path, "rb").read()
        host_url = self.server.OBJECT_STORAGE_SERVER_HOST
        if type == "video":
            contentType = "video/mp4"
        elif type == "image":
            contentType = "image/png"
        elif type == "gif":
            contentType = "image/gif"
        params = {
            "name": path,
            "oid": objId,
            "type": type,
            "ver": "2.0",
            "userid": self.profile.mid
        }
        if type == "gif":
            params.update({"type": "gif"})
        headers = {
            "accept": "*/*",
            "X-Line-ChannelToken": self.settings.get('channelToken').get('channelToken'),
            "x-lal": "en_GB",
            "x-line-signup-region": "ID",
            "content-type": contentType,
            "x-obs-params": self.genOBSParams(params, 'b64'),
            "X-Line-Carrier": "51010,0-19",
            "User-Agent": "Line/11.18.2",
            "connection": "Keep-Alive",
            "X-Line-Application": "ANDROID	11.18.2	Android OS	7.0",
            "cache-control": "no-cache",
            "X-Line-Mid": self.profile.mid,
        }
        if kwargs.get('updateCover'):
            if type == "video":
                headers.update({
                    "X-Line-PostShare": "True",
                    "X-Line-StoryShare": "True",
                    "x-line-signup-region": "US"
                })
                path_url = f"/r/myhome/vc/{objId}"
            elif type == "image":
                path_url = f"/myhome/c/upload.nhn"
        elif kwargs.get('updatePost'):
            path_url = f"/myhome/h/upload.nhn"
        elif kwargs.get('updateComment'):
            path_url = f"/r/myhome/cmt/{objId}"
        #if isinstance(data, bytes):
        r = await self.server.request('POST', host_url + path_url, 'text', content = data, headers = headers)
        #else:
        #    r = await self.server.request('POST', host_url + path_url, 'text', data = data, headers = headers)
        self.removeFile(path)
        if r.status_code == 201:
            if returnAs == "objId":
                return r.headers.get('x-obs-oid')
            elif returnAs == 'headers':
                return r.headers
            else:
                return True
        else:
            raise Exception("Upload object home failure.")