

class Config(object):

    TALK_SERVER_HOST                     = "https://ga2.line.naver.jp"
    FALLBACK_LEGY_HTTP2_HOST             = "https://gw.line.naver.jp"
    LINE_GWS_SERVER_HOST                 = "https://gws.line.naver.jp"
    OBJECT_STORAGE_SERVER_HOST           = "https://obs-sg.line-apps.com"
    OBS_CDN_SERVER_HOST                  = "https://obs.line-cdn.net"
    OBS_SCDN_SERVER_HOST                 = "https://obs.line-scdn.net"
    TALK_SERVER_HOST_SECONDARY           = "https://ga2k.line.naver.jp"
    LONG_POLLING                         = "/P5"
    NORMAL_POLLING                       = "/NP5"
    NORMAL                               = "/S4"
    COMPACT_MESSAGE                      = "/C5"
    COMPACT_PLAIN_MESSAGE                = "/CA5"
    COMPACT_E2EE_MESSAGE                 = "/ECA5"
    REGISTRATION                         = "/api/v4/TalkService.do"
    NOTIFY_SLEEP                         = "/F4"
    NOTIFY_BACKGROUND                    = "/B"
    BUDDY                                = "/BUDDY4"
    SHOP                                 = "/SHOP4"
    SHOP_AUTH                            = "/SHOPA"
    SHOP_RECOMMENDATION                  = "/EXT/sapi/sapir/v1p/strs"
    SHOP_LFL_PREMIUM                     = "/EXT/sapi/sapil/v1p/lps"
    UNIFIED_SHOP                         = "/TSHOP4"
    STICON                               = "/SC4"
    CHANNEL                              = "/CH4"
    CANCEL_LONGPOLLING                   = "/CP4"
    USER_BEHAVIOR_LOG                    = "/L1"
    AGE_CHECK                            = "/ACS4"
    SPOT                                 = "/SP4"
    CALL                                 = "/V4"
    EXTERNAL_INTERLOCK                   = "/EIS4"
    TYPING                               = "/TS"
    CONN_INFO                            = "/R2"
    PAY                                  = "/PY4"
    WALLET                               = "/WALLET4"
    AUTH                                 = "/RS4"
    AUTH_REGISTRATION                    = "/api/v4p/rs"
    SEARCH_COLLECTION_MENU_V1            = "/collection/v1"
    SEARCH_COLLECTION_MENU_V2            = "/collection/v2"
    SEARCH_V2                            = "/search/v2"
    SEARCH_V3                            = "/search/v3"
    BEACON                               = "/BEACON4"
    PERSONA                              = "/PS4"
    SQUARE                               = "/SQ1"
    SQUARE_BOT                           = "/BP1"
    POINT                                = "/POINT4"
    COIN                                 = "/COIN4"
    LIFF                                 = "/LIFF1"
    CHAT_APP                             = "/CAPP1"
    IOT                                  = "/IOT1"
    USER_PROVIDED_DATA                   = "/UPD4"
    NEW_REGISTRATION                     = "/acct/pais/v1"
    SECONDARY_QR_LOGIN                   = "/acct/lgn/sq/v1"
    SECONDARY_VERIFY_LOGIN               = "/acct/lp/lgn/sq/v1"
    LINE_SPOT                            = "/ex/spot"
    LINE_HOME_V2_SERVICES                = "/EXT/home/sapi/v4p/hsl"
    LINE_HOME_V2_CONTENTS_RECOMMENDATION = "/EXT/home/sapi/v4p/flex"
    BIRTHDAY_GIFT_ASSOCIATION            = "/EXT/home/sapi/v4p/bdg"
    SAFETY_CHECK                         = "/EXT/home/safety-check/safety-check"
    GLN_NOTIFICATION_STATUS              = "/gln/webapi/graphql"
    BOT_EXTERNAL                         = "/BOTE"
    E2EE_KEY_BACKUP                      = "/EKBS4"
    OA_MEMBERSHIP                        = "/EXT/oafan/api"

    PSYCHOPUMPUM = "1656442765-yjq3NdBQ"

    CHANNEL_ID = {
        'LINE_LIFF_ID'      : PSYCHOPUMPUM.split('-')[0],
        'LINE_TIMELINE'     : '1341209950',
        'LINE_HOME'         : '1341209850',
        'LINE_WEBTOON'      : '1401600689',
        'LINE_TODAY'        : '1518712866',
        'LINE_STORE'        : '1376922440',
        'LINE_MUSIC'        : '1381425814',
        'LINE_MUSIC_GLOBAL' : '1474176914',
        'LINE_SERVICES'     : '1459630796',
        'LINE_LIVE_VIEWER'  : '1525920906',
        'LINE_KEEP'         : '1433572998',
        'LINE_ALBUM'        : '1375220249',
        'LINE_NOTES'        : '1339901586',
        'LINE_FACE_PLAY'    : '1602114596',
        'LINE_TRANSLATE'    : '1627632136',
        'LINE_REWARD_COIN'  : '1370466387',
        'LINE_NOTIFICATIN'  : '1583881852',
        'LINE_EVENTS'       : '1506931000',
        'LINE_TRANSLATE'    : '1627632136',
        'LINE_AVATAR'       : '1653848125'
    }

    APP_VERSION = {
        "ANDROID"          : "12.18.1",
        "ANDROIDSECONDARY" : "12.18.1",
        "IOS"              : "12.17.1",
        "IOSIPAD"          : "12.17.1",
        "CHROMEOS"         : "2.5.7",
        "DESKTOPWIN"       : "7.12.0",
        "WATCHOS"          : "12.17.1",
        "WEAROS"           : "1.0.0",
        "DESKTOPMAC"       : "7.12.1",
        "CHANNELCP"        : "12.17.1"
    }

    SYSTEM_NAME = {
        "ANDROID"          : "Android OS",
        "ANDROIDSECONDARY" : "Android OS",
        "IOS"              : "iOS",
        "IOSIPAD"          : "iPadOS",
        "WATCHOS"          : "iOS",
        "CHROMEOS"         : "Chrome_OS",
        "DESKTOPWIN"       : "Windows OS",
        "DESKTOPMAC"       : "macOS",
        "WEAROS"           : "Android OS",
        "CHANNELCP"        : "iPadOS",
    }

    SYSTEM_VERSION = {
        "ANDROID"          : "7.0",
        "ANDROIDSECONDARY" : "7.0",
        "IOS"              : "15.2",
        "IOSIPAD"          : "15.2",
        "WATCHOS"          : "15.2",
        "DESKTOPWIN"       : "10",
        "DESKTOPMAC"       : "10.14",
        "WEAROS"           : "7.0",
        "CHROMEOS"         : "1",
        "CHANNELCP"        : "15.2",
    }

    CARRIER      = '51010,0-19'
    IP_ADDR      = '8.8.8.8'

    def __init__(self, appType=None, secondary=False):
        if appType:
            if appType == 'ANDROIDLITE':
                raise Exception("Application deprecated.")
            else:
                self.APP_NAME     = f"{appType}\t{self.APP_VERSION[appType]}\t{self.SYSTEM_NAME[appType]}\t{self.SYSTEM_VERSION[appType]}"
                self.USER_AGENT   = f"Line/{self.APP_VERSION[appType]}"
        else:
            self.APP_NAME         = "IOSIPAD\t12.17.1\tiPadOS\t15.2"
            self.USER_AGENT       = "Line/12.17.1"