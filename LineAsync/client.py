from .auth import Auth
from .talk import Talk
from .oepoll import OEPoll
from .handlers import Methods, Handler, BaseClient

import asyncio, sys
from concurrent.futures.thread import ThreadPoolExecutor

class Client(Auth, Talk, Methods, BaseClient):

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    def __init__(self, idOrAccessToken=None, passwd=None, **kwargs):
        self.accessToken   = kwargs.pop('accessToken', None)
        self.certificate   = kwargs.pop('certificate', None)
        self.appType       = kwargs.pop('appType', None)
        self.appName       = kwargs.pop('appName', None)
        self.secondary     = kwargs.pop('secondary', False)
        self.systemName    = kwargs.pop('systemName', None)
        self.keepLoggedIn  = kwargs.pop('keepLoggedIn', True)
        self.clientName    = kwargs.pop('clientName', None)
        self.clientMid     = kwargs.pop('clientMid', None)
        self.clientType    = kwargs.pop('clientType', None)
        self.proxy_host    = kwargs.pop("host", None)
        self.proxy_port    = kwargs.pop("port", None)
        self.timeout       = kwargs.pop("timeout", None)
        self._loop         = kwargs.pop("loop", asyncio.get_event_loop())
        self.workers       = kwargs.pop("workers", 2)
        self.executor      = ThreadPoolExecutor(self.workers, thread_name_prefix = "Handler")
        self.isLoggedIn    = False
        if self.proxy_host and self.proxy_port:
            self.proxies   = {"https": f"https://{self.proxy_host}:{self.proxy_port}"}
        else:
            self.proxies   = None
        Auth.__init__(self)
        if not self.appType and not self.appName:
            self.appType = "IOSIPAD"
        if idOrAccessToken and passwd:
            self.loginWithCredential(idOrAccessToken, passwd)
        elif idOrAccessToken and not passwd:
            try:
                self.accessToken = idOrAccessToken
                self.loginWithAccessToken()
                self.isLoggedIn = True
            except Exception as e:
                print(e)
                self._loop.run_until_complete(self.loginWithQrCode())
        elif not (idOrAccessToken or idOrAccessToken and passwd):
            self._loop.run_until_complete(self.loginWithQrCode())
        Talk.__init__(self)
        if self.isLoggedIn:
            self.poll        = OEPoll(self)

    def add_handler(self, type, callback, filters):
        if type not in self.poll.plug_handler.keys():
            self.poll.plug_handler[type] = [{callback: [filters, self]}]
        else:
            self.poll.plug_handler[type].append({callback: [filters, self]})

    """def initAll(self):
        Liff.__init__(self)
        Models.__init__(self)
        Shop.__init__(self)
        Talk.__init__(self)
        Timeline.__init__(self)
        Square.__init__(self)"""

    @property
    def printSuccess(self):
        ret  = f"{self.RED}─────── {self.RESET}• PSYCHOPUMPUM •{self.RED} ───────\n"
        ret += f"{self.CYAN}  • NAME : {self.BLUE}{self.profile.displayName}\n"
        ret += f"{self.CYAN}  • MID : {self.BLUE}{self.profile.mid}\n"
        ret += f"{self.CYAN}  • accessToken : {self.BLUE}{self.accessToken}\n"
        ret += f"{self.CYAN}  • certificate : {self.BLUE}{self.certificate}\n"
        ret += f"{self.CYAN}  • appname : {self.server.talkHeaders.get('X-Line-Application')}\n"
        ret += f"{self.CYAN}  • user-agent : {self.server.talkHeaders.get('User-Agent')}{self.RESET}"
        print(ret)