import re, inspect
from LineFrugal.ttypes import Message

class Filter:
    #source pyrogram.Filters
    def __call__(self, message):
        raise NotImplementedError

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)


class InvertFilter(Filter):
    def __init__(self, base):
        self.base = base

    async def __call__(self, client: "LineAsync.Client", message: Message):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(client, message)
        else:
            x = client._loop.run_in_executor(
                client.executor,
                self.base,
                client, message
            )
        return not x

class AndFilter(Filter):

    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, client: "LineAsync.Client", message: Message):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(client, message)
        else:
            x = await client._loop.run_in_executor(
                client.executor,
                self.base,
                client, message
            )

        # short circuit
        if not x:
            return False

        if inspect.iscoroutinefunction(self.other.__call__):
            y = await self.other(client, message)
        else:
            y = await client._loop.run_in_executor(
                client.executor,
                self.other,
                client, message
            )

        return x and y

class OrFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, client: "LineAsync.Client", message: Message):
        if inspect.iscoroutinefunction(self.base.__call__):
            x = await self.base(client, message)
        else:
            x = await client._loop.run_in_executor(
                client.executor,
                self.base,
                client, message
            )

        if x:
            return True

        if inspect.iscoroutinefunction(self.other.__call__):
            y = await self.other(client, message)
        else:
            y = await client._loop.run_in_executor(
                client.executor,
                self.other,
                client, message
            )

        return x or y


def create(name: str, func: callable, **kwargs) -> type:
    d = {"__call__": func}
    d.update(kwargs)
    return type(name, (Filter,), d)()

def byte2int(t):
    e = 0
    i = 0
    s = len(t)
    for i in range(s):
        e = 256 * e + t[i]
    return e


def bin2bytes(k):
    e = []
    for i in range(int(len(k) / 2)):
        _i = int(k[i * 2:i * 2 + 2], 16)
        e.append(_i)
    return bytearray(e)

class Filters:

    create = create
    prefix = [".", "/", "!"]

    #Messages
    text           = create("Text", lambda _,m: bool(m.contentType == 0 and m.text is not None))
    """Filter text messages."""

    image          = create("Image", lambda _,m: bool(m.contentType == 1))
    """Filter message that contain object Image"""

    video          = create("Video", lambda _,m: bool(m.contentType == 2))
    """Filter message that contain object Video"""

    audio          = create("Audio", lambda _,m: bool(m.contentType == 3))
    """Filter message that contain object Audio"""

    html           = create("Html", lambda _,m: bool(m.contentType == 4))
    """Filter message that contain object HTML"""

    pdf            = create("Pdf", lambda _,m: bool(m.contentType == 5))
    """Filter message that contain object PDF"""

    call           = create("Call", lambda _,m: bool(m.contentType == 6))
    """Filter calling from other"""

    sticker        = create("Sticker", lambda _,m: bool(m.contentType == 7))
    """Filter message that contain object Sticker"""

    gift           = create("Gift", lambda _,m: bool(m.contentType == 9))
    """Filter message that contain object Gift"""

    link           = create("Link", lambda _,m: bool(m.contentType == 12))
    """Filter message that contain object Link"""

    contact        = create("Contact", lambda _,m: bool(m.contentType == 13))
    """Filter message that contain object Contact"""

    files          = create("Files", lambda _,m: bool(m.contentType == 14))
    """Filter message that contain object Files"""

    location       = create("Location", lambda _,m: bool(m.contentType == 15))
    """Filter message that contain object Location"""

    post           = create("Post", lambda _,m: bool(m.contentType == 16))
    """Filter message that contain object Post"""

    rich           = create("Rich", lambda _,m: bool(m.contentType == 17))
    """Filter message that contain object Message Rich"""

    event          = create("Event", lambda _,m: bool(m.contentType == 18))
    """Filter message that contain object Event"""

    music          = create("Music", lambda _,m: bool(m.contentType == 19))
    """Filter message that contain object Music"""

    mention        = create("Mention", lambda _,m: bool('MENTION' in m.contentMetadata.keys()))
    """Filter message that contain object Mention"""

    reply          = create("Reply", lambda _,m: bool("reply" in m.contentMetadata.values() or "SRC_SVC_CODE" in m.contentMetadata.keys()))
    """Filter message that are Reply"""

    #TODO: Forward only worked for text type, i cant found clue to catch forward media as image,video,audio
    forward        = create("Forward", lambda _,m: bool("forward" in m.contentMetadata.values()))
    """Filter message that are Forwarded"""

    #Grouping
    group          = create("Group", lambda _,m: bool(m.toType == 2))
    private        = create("Private", lambda _,m: bool(m.toType == 0))
    room           = create("Room", lambda _,m: bool(m.toType == 1))

    #Event
    flex           = create("Flex", lambda _,m: bool(m.contentType == 22 and "FLEX_JSON" in m.contentMetadata.keys()))
    image_carousel = create("ImageCarousel", lambda _,m: bool(Filters.html and m.contentMetadata["HTML_CONTENT"] != None))


    @staticmethod
    def command(commands: str or list, prefix: str or list = prefix, separator: str = "|", case_sensitive: bool = False):
        """
        Filter commands, i.e.: text messages starting with "/" or any other custom prefix.
            Args:
                command (``str`` | ``list``):
            The command or list of commands as string the filter should look for.
                Examples: "start", ["start", "help", "settings"]. When a message text containing
                a command arrives, the command itself and its arguments will be stored in the *command*
                field of the :class:`Message <akad.ttypes.Message>`.
            prefix (``str`` | ``list``, *optional*):
                A prefix or a list of prefixes as string the filter should look for.
                Defaults to "/" (slash). Examples: ".", "!", ["/", "!", "."].
                Can be None or "" (empty string) to allow commands with no prefix at all.
            separator (``str``, *optional*):
                The command arguments separator. Defaults to " " (white space).
                Examples: /start first second, /start-first-second, /start.first.second.
            case_sensitive (``bool``, *optional*):
                Pass True if you want your command(s) to be case sensitive. Defaults to False.
                Examples: when True, command="Start" would trigger /Start but not /start.
        """

        def f(_, m):
            m.command = []
            if m.text:
                for i in _.p:
                    if m.text:
                        if m.text.startswith(i) or m.text.startswith(f"{i} "):
                            t = m.text.split(_.s)
                            c, a = t[0][len(i):] if m.text.startswith(i) and not m.text.startswith(f"{i} ") else t[0][len(f"{i} "):], t[1:] if m.text.startswith(i) else t[2:]
                            c = c if _.cs else c.lower()
                            m.command = ([c] + a) if c in _.c else None
            elif not m.text and m.contentMetadata.get('e2eeVersion') == '2' and m.chunks:
                chunks = m.chunks
                for i in range(len(chunks)):
                    if isinstance(chunks[i], str):
                        chunks[i] = chunks[i].encode()
                senderKeyId = byte2int(chunks[3])
                receiverKeyId = byte2int(chunks[4])
            return bool(m.command)
        return create("Command", f, c = {commands if case_sensitive else commands.lower()} if not isinstance(commands, list) else {c if case_sensitive else c.lower() for c in commands}, p=set(prefix) if prefix else {""}, s=separator, cs=case_sensitive)

    @staticmethod
    def regex(pattern, flags: int = 0):
        """Filter messages that match a given RegEx pattern
        Args:
            pattern (``str``):
                The RegEx pattern as string, it will be applied to the text of a message. When a pattern matches,
                all the `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`

            flags (``int``, *optional*):
                RegEx flags.
        """
        def f(_, m):
            tt = ""
            for pp in Filters.prefix:
                if m.text:
                    if not m.text.startswith(pp):
                        continue
                    else:
                        tt = m.text if m.text.startswith(f"{pp}") else ""
                else:
                    return False
            m.matches = [i for i in _.p.finditer(tt or "")]
            return bool(m.matches)
        return create("Regex", f, p=re.compile(pattern, flags))

class user(Filter, set):
    """
        Filter messages coming from one or more users.		
        You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html#set>`_ to manipulate the users container.
	      Args:
	        users (``str`` | ``list``):
	          Pass one or more user mid to filter users.
	          Defaults to None (no users).
    """
    def __init__(self, users: int or str or list = None):
        users = [] if users is None else users if isinstance(users, list) else [users]
        super().__init__({i.lower() if isinstance(i, str) else i for i in users} if isinstance(users, list) else {users.lower() if isinstance(users, str) else user})

    def __call__(self, message):
        return bool(message.from_ and (message.from_ in self))

class chat(Filter, set):
    """
        Filter messages coming from one or more chats.
        You can use `set bound methods <https://docs.python.org/3/library/stdtypes.html#set>`_ to manipulate the chats container.
	      Args:
	          chats (``str`` | ``list``):
	              Pass one or more chat mid to filter chats.
	              Defaults to None (no chats).
    """
    def __init__(self, chats: int or str or list = None):
        chats = [] if chats is None else chats if isinstance(chats, list) else [chats]
        super().__init__({i.lower() if isinstance(i, str) else i for i in chats} if isinstance(chats, list) else {chats.lower() if isinstance(chats, list) else chats})

    def __call__(self, message):
        return bool(message.toType in [1, 2] and (message.to in self))