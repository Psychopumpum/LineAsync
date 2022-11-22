#!usr/bin/python
# -*- coding: utf-8 -*-
#from httplib2 import Response, Http
#from struct import pack, unpack
import traceback, sys, httpx
from .object import Object
#from LineThriftService.ttypes import TalkException

import shutil, time, os, json
import base64, tempfile

from random import randint

from io import BytesIO

class TType(object):
    STOP = 0
    VOID = 1
    BOOL = 2
    BYTE = 3
    I08 = 3
    DOUBLE = 4
    I16 = 6
    I32 = 8
    I64 = 10
    STRING = 11
    UTF7 = 11
    STRUCT = 12
    MAP = 13
    SET = 14
    LIST = 15
    UTF8 = 16
    UTF16 = 17

class CompactType(object):
    STOP = 0x00
    TRUE = 0x01
    FALSE = 0x02
    BYTE = 0x03
    I16 = 0x04
    I32 = 0x05
    I64 = 0x06
    DOUBLE = 0x07
    BINARY = 0x08
    LIST = 0x09
    SET = 0x0A
    MAP = 0x0B
    STRUCT = 0x0C
    
CTYPES = {
    TType.STOP: CompactType.STOP,
    TType.BOOL: CompactType.TRUE,
    TType.BYTE: CompactType.BYTE,
    TType.I16: CompactType.I16,
    TType.I32: CompactType.I32,
    TType.I64: CompactType.I64,
    TType.DOUBLE: CompactType.DOUBLE,
    TType.STRING: CompactType.BINARY,
    TType.STRUCT: CompactType.STRUCT,
    TType.LIST: CompactType.LIST,
    TType.SET: CompactType.SET,
    TType.MAP: CompactType.MAP,
}

TTYPES = {}
for k, v in CTYPES.items():
    TTYPES[v] = k
TTYPES[CompactType.FALSE] = TType.BOOL
del k
del v

class DummyProtocolData():

    def __init__(self, id, type, data, subType: list = None):
        self.id = id
        self.type = type
        self.data = data
        self.subType = []
        if subType is not None:
            for _subType in subType:
                self.addSubType(_subType)

    def addSubType(self, type):
        self.subType.append(type)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))


class Models(Object):

    def __init__(self):
        self.last_fid = 0
        self.last_pos = 0
        self.last_sid = 0

    def removeFolder(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)

    def removeFile(self, path):
        if os.path.exists(path):
            os.remove(path)

    def saveFile(self, path, raw):
        with open(path, 'wb') as f:
            shutil.copyfileobj(raw, f)

    def genTempFile(self, returnAs='path'):
        try:
            if returnAs not in ['file','path']:
                raise Exception('Invalid returnAs value')
            fName, fPath = 'LineClient-%s-%i.bin' % (int(time.time()), randint(0, 9)), tempfile.gettempdir()
            if returnAs == 'file':
                return fName
            elif returnAs == 'path':
                return os.path.join(fPath, fName)
        except:
            raise Exception('tempfile is required')

    def genOBSParams(self, newList, returnAs='json', ext='jpg'):
        oldList = {'name': f'LineClient-{int(time.time())}.{ext}','ver': '1.0'}
        if returnAs not in ['json','b64','default']:
            raise Exception('Invalid parameter returnAs')
        oldList.update(newList)
        if returnAs == 'json':
            oldList = json.dumps(oldList)
            return oldList
        elif returnAs == 'b64':
            oldList = json.dumps(oldList)
            return base64.b64encode(oldList.encode('utf-8'))
        elif returnAs == 'default':
            return oldList

    async def downloadObjectMsg(self, messageId, returnAs="path", saveAs="", original=False, headers = {}):
        if saveAs == "":
            saveAs = self.genTempFile()
        if returnAs not in ["path", "bool", "bin"]:
            raise Exception("Invalid returnAs value")
        headers = headers if headers else self.server.talkHeaders
        params = {"oid": messageId}
        if messageId.isdigit():
            url = self.server.OBJECT_STORAGE_SERVER_HOST + f"/talk/m/download.nhn"
            if original:
                params["tid"] = "original"
        else:
            url = messageId
            params = {}
        r = await self.server.request('GET', url, 'text', params = params, headers = headers)
        if r.status_code == 200:
            self.saveFile(saveAs, BytesIO(r.content))
            if returnAs == "path":
                return saveAs
            elif returnAs == "bool":
                return True
            elif returnAs == "bin":
                return r.raw
        else:
            raise Exception("Download object failure.")

    def zipping(self, to, path = None, output = None):
        os.system('py3clean .')
        self.removeFile(f"{path}.zip")
        time.sleep(1)
        zipf = shutil.make_archive(output, 'zip', path)

    def setRevision(self, revision):
        self.revision = max(revision, self.revision)

    def fetchOps(self, count = 100, p5 = True):
        if not p5:
            try:
                operations = self.poll.fetchOps(self.revision, count, self.globalRev, self.individualRev)
            except TalkException as e:
                if e.code == 8:
                    sys.exit(e.reason)
            except KeyboardInterrupt:
                sys.exit('Oops (┛◉Д◉)┛彡┻━┻')
            except:
                return []
            return operations
        params = [
            [10, 2, self.revision],
            [8, 3, count],
            [10, 4, self.globalRev],
            [10, 5, self.individualRev]
        ]
        data = [130, 33, 00, 8, 102, 101, 116, 99, 104, 79, 112, 115]
        for param in params:
            _type, _id, _data = param[0], param[1], param[2]
            if not _data:continue
            data += self.getFieldHeader(CTYPES[_type], _id)
            if _type == 8:
                data += self.getIntBytes(_data, isCompact = True)
            if _type == 10:
                data += self.getIntBytes(_data, 8, True)
        client = Http() if self.appType != "ANDROID" else httpx.Client(base_url = "https://ga2.line.naver.jp", http2=True)
        hr = self.server.additionalHeaders(self.server.talkHeaders, {
            "x-lam": "w",
            "x-las": "F",
            "accept": "application/x-thrift",
            "x-lap": "5",
            "Content-Type": "application/x-thrift; protocol=TCOMPACT"
        })
        if self.appType == "ANDROID":
            r = client.build_request("POST", "/P5", content = bytes(data + [0]), headers = hr, timeout = None)
            req = client.send(r)
            response = req.read()
        else:
            headers, response = client.request("https://ga2.line.naver.jp:443/P5", "POST", body = bytes(data + [0]), headers = hr)
        if not response:
            return []
        try:
            res = self.TMoreCompactProtocol(response).res
            if 'error' in res:
                if res["error"].get("code") == 8:
                    sys.exit(res["error"].get("message"))
            return res
        except Exception as e:
            traceback.print_exc()

    def updateChats(self, chatMid, chatSet, updatedAttribute=1):
        sqrd = [128, 1, 0, 1, 0, 0, 0, 10, 117, 112, 100, 97, 116, 101, 67, 104, 97, 116, 0, 0, 0, 0, 12, 0, 1, 8, 0, 1, 0, 0, 0, 0, 12, 0, 2]
        if chatSet.get(1) is not None:
            sqrd += [8, 0, 1] + self.getIntBytes(chatSet[1])
        else:
            sqrd += [8, 0, 1, 0, 0, 0, 1]  # type
        sqrd += [11, 0, 2] + self.getStringBytes(chatMid)
        if chatSet.get(4) is not None:
            sqrd += [2, 0, 4, int(chatSet[4])]
        if chatSet.get(6) is not None:
            sqrd += [11, 0, 6] + self.getStringBytes(chatSet[6])
        if chatSet.get(8) is not None:
            extra = chatSet[8]
            sqrd += [12, 0, 8]
            sqrd += [12, 0, 1]
            if extra.get(2) is not None:
                sqrd += [2, 0, 2, int(extra[2])]
            if extra.get(6) is not None:
                sqrd += [2, 0, 6, int(extra[6])]
            if extra.get(7) is not None:
                sqrd += [2, 0, 7, int(extra[7])]
            sqrd += [0, 0]
        sqrd += [0]
        sqrd += [8, 0, 3] + self.getIntBytes(updatedAttribute)
        sqrd += [0, 0]
        client = Http() if self.appType != "ANDROID" else httpx.Client(base_url = "https://ga2.line.naver.jp", http2=True)
        hr = self.server.additionalHeaders(self.server.talkHeaders, {
            "accept": "application/x-thrift",
            "Content-Type": "application/x-thrift; protocol=TCOMPACT"
        })
        headers, response = client.request("https://ga2.line.naver.jp:443/S4", "POST", body = bytes(sqrd), headers = hr)

    def updateChatPreventedUrl(self, chatMid, bool):
        return self.updateChats(chatMid, {8: {2: bool}}, 4)
 
    def getIntBytes(self, i, l = 4, isCompact = False):
        i = int(i)
        if isCompact:
            a = self.makeZigZag(i, 32 if l ** 2 == 16 else 64)
            b = self.writeVarint(a)
            return b
        if l**2 == 16:
            res = pack("!i", i)
        else:
            res = pack("!q", i)
        return list(res)

    def getStringBytes(self, text = None, isCompact = False):
        if not text:
            text = ""
        if type(text).__name__ == "bytes":
            pass
        else:
            text = text.encode()
        if isCompact:
            sqrd = self.writeVarint(len(text))
        else:
            sqrd = self.getIntBytes(len(text))
        for value in text:
            sqrd.append(value)
        return sqrd

    def getFieldHeader(self, type, fid):
        delta = fid - self.last_fid
        res = []
        if 0 < delta <= 15:
            res.append(delta << 4 | type)
        else:
            res += list(pack("!b", type))
            res += self.writeVarint(self.makeZigZag(fid, 16))
        self.last_fid = fid
        return res

    def makeZigZag(self, n, bits):
        return (n << 1) ^ (n >> (bits - 1))

    def writeVarint(self, data):
        out = []
        while True:
            if data & ~0x7f == 0:
                out.append(data)
                break
            else:
                out.append((data & 0xff) | 0x80)
                data = data >> 7
        return out

    def readVarint(self, data):
        a, b = 0, 0
        while True:
            l = data[self.last_pos]
            self.last_pos += 1
            a |= (l & 127) << b
            if (l & 128) != 128:
                return a
            b += 7