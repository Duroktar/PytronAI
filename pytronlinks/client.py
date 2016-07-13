# -*- coding: UTF-8 -*-

"""
    Pytron - The MVC Links Interface
    ~~~~~~

    Links for Python. Interact with Links from your scripts!

     http://mega-voice-command.com/

    :copyright: (c) 2016 by traBpUkciP.
    :license: BSD, see LICENSE for more details.
"""

from time import sleep
import time
import datetime
import urllib


class Client(object):
    """A Python client for the Mega Voice Command AI LINKS-MarkII

         http://mega-voice-command.com/

    """

    def __init__(self, path, port='54657', key='ABC1234', ip='localhost'):
        """A client for the Facebook Chat (Messenger).

        :param port: Port that links is listening on
        :param key: Links web key
        :param ip: ip of computer with links
        :param path: Path to Links Scripts Folder ( MUST BE RAW ) ie: (r'PATH')
          ex: ai = pytronlinks.Client(path='C:\\temp', ip='176.0.0.16', key='NeWkEy123')

        :Example:

            import pytronlinks

            path = (r'C:\users\default\AppData\Roaming\LINKS\Customization\Scripts')
            ai = pytronlinks.Client(path)


        """
        self.path = path
        self.ip = ip
        self.port = port
        self.key = key
        self._clear_input()

    def talk(self, text):
        """ Speaks through Links

        :param text: String to be spoken

        :Example:

            import pytronlinks

            PATH = (r'C:\users\default\AppData\Roaming\LINKS\Customization\Scripts')
            TEXT = ('MVC Rocks!')

            ai = pytronlinks.Client(PATH)
            ai.talk(TEXT)

        """
        try:
            ip = self.ip
            port = self.port
            key = self.key
            fcn = '[Speak("{}")]'.format(text)
            url = 'http://{}:{}/?action={}&key={}&request=enable'.format(ip, port, fcn, key)
            urllib.urlopen(url)
        except Exception as e:
            print(e)
            return

    def emulate_speech(self, command):
        """ Sends an Emulate Speech Command

        :param command: This is the speech for the command you want to emulate
        :return:

        :Example:
            import pytronlinks

            PATH = (r'C:\users\default\AppData\Roaming\LINKS\Customization\Scripts')
            TEXT = ('what is the weather like')

            ai = pytronlinks.Client(PATH)
            ai.emulate_speech(TEXT)

        Will call the command as if you had spoken to links directly
        """
        try:
            ip = self.ip
            port = self.port
            key = self.key
            fcn = '[EmulateSpeech("{}")]'.format(command)
            url = 'http://{}:{}/?action={}&key={}&request=enable'.format(ip, port, fcn, key)
            urllib.urlopen(url)
        except (TypeError, IOError, Exception):
            print("Exception in talk function")
            return

    def listen(self, freq=0.2):
        """ Actively checks for user Input and returns that input when found. ( BLOCKING )

        :param freq: Delay ( in seconds ) between checks for user input in dictation.txt

        :Example:

            import pytronlinks

            PATH = (r'C:\users\default\AppData\Roaming\LINKS\Customization\Scripts')
            ai = pytronlinks.Client(PATH)

            def main():
                dictation = listen()
                if x:
                    ( do something with dictation )
                    return

            try:
                while True:
                    main()
            except KeyboardInterrupt:
                pass
        """
        print("Awaiting commands")
        while True:
            x = self.check_for_input()
            if x:
                print(x)
                return str(x)
            else:
                sleep(freq)
                continue

    def check_for_input(self):
        """ Check dictation file for changes """
        with open(self.path + "\dictation.txt", 'r') as f:
            for line in f:
                dictation = line
                f.close()
                if dictation:
                    self._write_history(dictation)
                    self._clear_input()
                    return dictation
                else:
                    return False

    def _clear_input(self):
        """ Deletes any entries in dictation file. Also used to create new file on init. -private """
        with open(self.path + '\dictation.txt', 'w+') as f:
            f.close()

    def _write_history(self, text):
        """ Appends history.txt with detected user input -private

        :param text:
        """
        secs = time.time()
        time_stamp = datetime.datetime.fromtimestamp(secs).strftime('%Y-%m-%d %H:%M:%S')
        history = "{}: {}".format(time_stamp, text)
        with open(self.path + '\history.txt', 'a') as f:
            f.write(history)
            f.close()

    @staticmethod
    def strip_non_ascii(string):
        """ Can be used to remove non-ascii characters from a string.

        :param string: String with non-ascii characters
        :return: Cleaned up string
        """
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    @staticmethod
    def strip_bad_chars(string):
        """ Cleans up some speech elements.. Replaces some things that may otherwise
           mess up the url request to Links.. ( this function is ugly and needs a bag on its head )

        :type string: String with characters to be replaced
        """
        bad_chars = '[]=^_'  # Characters to remove outright
        a = "".join(c for c in string if c not in bad_chars)
        a = a.replace("~~", " approximately ")  # Helps format the way certain sites return math values
        a = a.replace(";", ",")  # Gets rid of semi-colons
        return a
