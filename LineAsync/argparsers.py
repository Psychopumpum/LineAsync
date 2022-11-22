# -*- coding: utf-8 -*-
import argparse, sys, gettext

Args = [
    {
        'short_name': '-n',
        'long_name': '--name',
        'help': 'any name you want to give to your pyrogram.Client',
        'type': str
    },
    {
        'short_name': '-u',
        'long_name': '--mid',
        'help': 'a userid classify to give to your pyrogram.Client',
        'type': str
    },
    {
        'short_name': '-c',
        'long_name': '--certificate',
        'help': 'certificate are using for bypassing qrcode (with enter pincode when logged in)',
        'type': str
    },
    {
        'short_name': '-t',
        'long_name': '--token',
        'help': 'the bots accessToken for accessing the API',
        'type': str
    },
    {
        'short_name': '-a',
        'long_name': '--apptype',
        'help': 'the application type of accessToken',
        'type': str
    }
]

class ColoredArgumentParser(argparse.ArgumentParser):

    color_dict = {
        'RED' : '1;31',
        'GREEN' : '1;32',
        'YELLOW' : '1;33',
        'BLUE' : '1;36'
    }

    def print_usage(self, file = None):
        if file is None:
            file = sys.stdout
        self.log(self.format_usage()[0].upper() + 
                            self.format_usage()[1:],
                            file, self.color_dict['YELLOW'])

    def print_help(self, file = None):
        if file is None:
            file = sys.stdout
        self.log(
            self.format_help()[0].upper() + self.format_help()[1:],
            file,
            self.color_dict['BLUE']
        )

    def log(self, message, file = None, color = None):
        if message:
            if file is None:
                file = sys.stderr
            if color is None:
                file.write(message)
            else:
                file.write('\x1b[' + color.upper() + 'm' + message.strip() + '\x1b[0m\n')

    def exit(self, status = 0, message = None):
        if message:
            self.log(message, sys.stderr, self.color_dict['RED'])
        sys.exit(status)

    def error(self, message):
        self.print_usage(sys.stderr)
        args = {'prog' : self.prog, 'message': message}
        self.exit(2, gettext.gettext('%(prog)s: Error: %(message)s\n') % args)