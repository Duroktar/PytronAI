# -*- coding: UTF-8 -*-

"""
    Pytron - The MVC Links Interface
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Links for Python. Interact with Links from your scripts!

     http://mega-voice-command.com/

"""

import os
from time import sleep, time
import datetime
import urllib
import xml.etree.ElementTree as ET
import ast


class Client(object):
    """ Main Pytron Client v.0.3.3

         :Example:

              import pytronlinks

               ai = pytronlinks.Client()

    """

    _APPDATA = os.getenv(r'APPDATA')
    _SCRIPTS_PATH = _APPDATA + r'\LINKS\Customization\Scripts'
    _XML_PATH = _APPDATA + r'\LINKS\Customization\XML'

    def __init__(self, path=_XML_PATH, port='54657', key='ABC1234', ip='localhost'):
        """ Initialize Client, either with custom parameters or the common default values

        :param port: Port that links is listening on
        :param key: Links web key
        :param ip: ip of computer with links
        :param path: If you installed links in a different location,
                     point this to the Scripts folder( MUST BE RAW ) ie: (r'PATH')

          ex: ai = pytronlinks.Client(path=r'C:\temp', ip='176.0.0.16', key='NeWkEy123')

        :Example:

            import pytronlinks

            ai = pytronlinks.Client()

        """
        try:
            self.path = path
            self.ip = ip
            self.port = port
            self.key = key
            self._clear_input()
        except Exception as e:
            print(e)
            print("It's not the end of the world.. But it's close. Try harder next time.")

    def talk(self, text):
        """ Speaks through Links

        :param text: String to be spoken

        :Example:

            import pytronlinks


            ai = pytronlinks.Client(PATH)
            ai.talk("Links is the best!")

        """
        try:
            fcn = '[Speak("{}")]'.format(text)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            return

    def emulate_speech(self, command):
        """ Sends an Emulate Speech Command

        :param command: This is the speech for the command you want to emulate

        Will call the command as if you had spoken to links directly
        *Listening must be enabled on Links! ( ie: Hard listening mode not disabled )

        :Example:
            import pytronlinks


            ai = pytronlinks.Client()

            ai.emulate_speech("what time is it")
            ai.emulate_speech("play music")


        """
        try:
            fcn = '[EmulateSpeech("{}")]'.format(command)
            self._get_request(fcn)
        except (TypeError, IOError, Exception):
            print("Exception in EmulateSpeech function")
            return

    def custom(self, string):
        """ Insert your own Links Action Commands.
                Anything you can put in Links *Action* bar, you can put in here! See example.

        :param string: See example..

        Example -

            import pytronlinks


            ai = pytronlinks.Client()

            ai.custom(r'[Set("Last Subject", "pytron is the coolest")]')
            ai.custom(r'[Speak("[Get("Last Subject")]")]')
        """
        self._get_request(string)
        return

    # Checks for any value in the UserVariables.xml file and returns it input when found. ( BLOCKING )
    def listen(self, var_name='Pytron', freq=0.2):
        """ Check out the example to see how you could use this. This is probably the most powerful feature.

        :param var_name: Name of the Variable you want to "listen" to. OPTIONAL. Defaults to 'Pytron'
        :param freq: Delay ( in seconds ) between checks. OPTIONAL. Defaults to 0.2 seconds



            ** Make a command in links social tab like this **
         Command: Links {speech=test_dictation}
         Response: [Set("Pytron", {speech})]
         Profile: Main

         And use the dictation in Pytron with the script below.. ( Ctrl-c to quit )
            v        v         v         v         v

        :Example:

            import pytronlinks

            ai = pytronlinks.Client()

            def main():
                dictation = listen()
                if dictation:
                    # ( do something with dictation )
                    print(dictation)
                    return

            try:
                while True:
                    main()
            except KeyboardInterrupt:
                pass
        """
        try:
            self._clear_xml(var_name)
            print("Awaiting commands")
            while True:
                x = self._get_xml()
                if x:
                    answer = x
                    self._clear_xml(var_name)
                    return answer
                else:
                    sleep(freq)
        except Exception as e:
            print("Exception in listen function! Get under the desk quick!")
            print(e)

    def config(self):
        """ Config itself doesn't work yet and for now just prints this handy - Volume and Rate Cheat-Sheet -

        Usage:
            import pytronlink
            ai = pytronlinks.Client()
            ai.config()

         *** The following strings or nums can be used to set voice parameters for any speak/task function. ***
        Volume:
             Silent = 0,
             ExtraSoft <= 20,
             Soft <= 4,
             Medium <= 60,
             Loud <= 80,
             ExtraLoud <= 100 (default)
             Leave it blank for default

        Rate:
             NotSet = 0
             ExtraFast = 1
             Fast = 2
             Medium = 3 (default)
             Slow = 4
             ExtraSlow = 5
             Leave it blank for default
        """
        print(self.config.__doc__)
        pass

    def LoqSpeak(self, text, volume, rate, ai_name):
        """ Sends a 'Loquendo by Nuance' speech command ( requires Nuance Loquendo voices )

        :param text: Text to be spoken ( with all the syntax they use, better make it raw, ie: r'text' )
        :param volume: Volume 0 - 100
        :param rate: Unsure of rate   ( needs testing )
        :param ai_name: Name of tts Voice ( case sensitive )
        """
        try:
            fcn = '[LLoquendo.Speech.Speak("{}", "{}", "{}", "{}")]'.format(text, volume, rate, ai_name)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in LoqSpeak function")
            return

    def Get(self, var_name):
        """ Gets a variable saved in the '\LINKS\Customization\XML\UserVariables.xml' file.

        :param var_name: Name of variable to get the value of
        :return: Returns the value of the variable
        """
        try:
            fcn = '[Get("{}")]'.format(var_name)
            self._get_request(fcn)
            return self._get_xml(var_name)
        except Exception as e:
            print(e)
            print("Exception in Get function")
            return

    def Set(self, var_name, var_value):
        """ Sets a variable in the '\LINKS\Customization\XML\UserVariables.xml' file.

        :param var_name: Name of variable
        :param var_value: Value to set
        """
        try:
            fcn = '[Set("{}", "{}")]'.format(var_name, var_value)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in Set function")
            return

    def SayAs(self, before, data, content, after=""):
        """ This function is only for speech. Will speak the appropriate way for the given data type. ( See example )

        :param before: In the example, the before string is "The phone number is" ( can be blank )
        :param after: In the example, the after string is "how cool is that?" ( defaults to blank )
        :param data: Data to be spoken as
        :param content: Data content type ( see https://msdn.microsoft.com/en-us/library/system.speech.synthesis.sayas(v=vs.110).aspx )

        Example:
        http://localhost:54657/?action=[Speak(%22The%20phone%20number%20is%20[SayAs(%2218001239874%22,%22Telephone%22)]%22)]&key=ABC1234
            ai.SayAs(r"The phone number is","18001239874","Telephone","how cool is that?")
        """
        try:
            fcn = '[Speak("{} [SayAs("{}","{}")]. {}")]'.format(before, data, content, after)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in SayAs function")
            return

    def SetSpeechVolume(self, vol):
        """ Sets system wide speech volume

        :param vol: 0 - 100
        """
        try:
            fcn = '[SetSpeechVolume("{}")]'.format(vol)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in SetSpeechVolume function")
            return

    def SetSpeechVoice(self, name):
        """ Set active speaker

        :param name: Name of tts speaker ( ex: IVONA Brian ) case sensitive
        """
        try:
            fcn = '[SetSpeechVoice("{}")]'.format(name)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in SetSpeechVoice function")
            return

    def SetSpeechConfig(self, name, vol, rate):
        """ Config a certain speakers parameters

        :param name: Name of tts speaker ( ex: IVONA Brian ) case sensitive
        :param vol: Volume 0 - 100
        :param rate: Speech rate -10 - 10
        """
        try:
            fcn = '[SetSpeechConfig("{}", "{}", "{}")]'.format(name, vol, rate)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in SetSpeechConfig function")
            return

    def SpeakEx(self, phrase, name, vol, rate, delay, sys_or_voice_vol="voice"):
        """ Speaks using specified values

        :param phrase: Phrase to be spoken
        :param name: Name of tts speaker ( ex: IVONA Brian ) case sensitive
        :param vol: 0 - 100
        :param rate: Fast - Slow
        :param delay: Initial delay
        :param sys_or_voice_vol: Use system wide volume or ai' set volume
        """
        try:
            fcn = '[SpeakEx("{}", "{}", "{}", "{}", "{}", "{}")]'.format(phrase, name, vol, rate, delay, sys_or_voice_vol)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in SpeakEx function")
            return

    def StopVoiceByName(self, name, ResponseOnSuccess):
        """ Stop the current speaker by AI name

        :param name: Name of ai ( case sensitive )
        :param ResponseOnSuccess: What the ai says after being silenced
        """
        try:
            fcn = '[StopVoiceByName("{}", "{}")]'.format(name, ResponseOnSuccess)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in StopVoiceByName function")
            return

    def StopVoiceByIdentifier(self, identifier, ResponseOnSuccess):
        """ Stops voice by Identifier, which is only set in tasks atm - uses tasks name

        :param identifier: Task name
        :param ResponseOnSuccess: AIs response
        """
        try:
            fcn = '[StopVoiceByIdentifier("{}", "{}")]'.format(identifier, ResponseOnSuccess)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in StopVoiceByIdentifier function")
            return

    def SpeakExSysVolSync(self, phrase, VoiceVolume, VoiceRate, phraseDelay, VoiceName):
        """ Synchronous speech

        :param phrase: Phrase to be spoken
        :param VoiceVolume: 0 - 100
        :param VoiceRate: -10 - 10
        :param phraseDelay: Delay between next speech ( ex: 0.8 )
        :param VoiceName: Ai name ( case sensitive )
        """
        try:
            fcn = '[SpeakExSysVolSync("{}", "{}", "{}", "{}", "{}")]'.format(phrase, VoiceVolume, VoiceRate,
                                                                     phraseDelay, VoiceName)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in SpeakExSysVolSync function")
            return

    def SpeakExSysVolAsync(self, phrase, VoiceVolume, VoiceRate, phraseDelay, VoiceName):
        """ Asynchronous speech

        :param phrase: Phrase to be spoken
        :param VoiceVolume: 0 - 100
        :param VoiceRate: -10 - 10
        :param phraseDelay: Delay between next speech ( ex: 0.8 )
        :param VoiceName: Ai name ( case sensitive )
        """
        try:
            fcn = '[SpeakExSysVolAsync("{}", "{}", "{}", "{}", "{}")]'.format(phrase, VoiceVolume, VoiceRate,
                                                                              phraseDelay, VoiceName)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            print("Exception in SpeakExSysVolAsync function")
            return

    def _get_xml(self, var_name='Pytron'):
        """ Checks xml file for incoming commands sent from links using the [Set("var", "value")] function
        and returns them.

        :param variable: Name of the variable in the UserVariable.xml file.
        :return: Returns the value of the variable.
        """
        try:
            self.variable = var_name
            _path = self.path + r'\UserVariables.xml'
            tree = ET.parse(_path)
            root = tree.getroot()
            response = False
            for variable in root.findall('Variable'):
                n = variable.find('Name').text
                if n == var_name:
                    v = variable.find('Value')
                    t = v.text
                    response = t
                    break
            return response
        except Exception as e:
            print("Exception in _get_xml function")
            print(e)
            return

    def _clear_xml(self, var_name='Pytron'):
        """ Clears xml value with pythons standard xml library ET

        :param var_name: Variable name in xml file
        """
        try:
            _path = self.path + r'\UserVariables.xml'
            tree = ET.parse(_path)
            root = tree.getroot()
            for variable in root.findall('Variable'):
                n = variable.find('Name').text
                if n == var_name:
                    v = variable.find('Value')
                    v.clear()
                    break
            tree.write(_path)
            return
        except Exception as e:
            print("Exception in _clear_xml function")
            print(e)
            return

    def _check_for_input(self):
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

    def _get_request(self, fcn):
        """ Speak to Links with a get request using urllib

        :param fcn: The function call for Links ( must be a valid links function )
        """
        try:
            ip = self.ip
            port = self.port
            key = self.key
            url = 'http://{}:{}/?action={}&key={}&request=enable&output=json'.format(ip, port, fcn, key)
            r = urllib.urlopen(url, context="'application/json")
            if r.code and r.code == 200:
                x = r.readlines()[3]
                j = ast.literal_eval(x)
                err = (j['error'])
                if len(err) > 0:
                    print("v" * 20)
                    res = (j['response'])
                    z = err + "\n" + res
                    print(z)
                    print("^" * 20)
                    print("\n")
                    return False
                else:
                    return
            elif r.code:
                print('Error {}'.format(r.code))
            else:
                print("Something went terribly wrong.....")
        except Exception as e:
            print("***Exception in _get_request function. Check your ip, port and key settings!***")
            print("Also your shoes are untied..")
            print("Exception: " + str(e))
            return

    def _write_history(self, text):
        """ Appends history.txt with detected user input -private

        :param text:
        """
        try:
            secs = time()
            time_stamp = datetime.datetime.fromtimestamp(secs).strftime('%Y-%m-%d %H:%M:%S')
            history = "{}: {}".format(time_stamp, text)
            with open(self.path + '\history.txt', 'a') as f:
                f.write(history)
                f.close()
        except Exception as e:
            print(e)
            print("Exception in _write_history function")

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


if __name__ == '__main__':
    ai = Client()
    ai.talk('Hello')
    ai.Set('Pytron', 'This is the first test')
    test = ai.Get('Pytron')
    ai.talk(test)
    ai.Set('Pytron', 'This is the second test')
    test = ai.Get('Pytron')
    ai.talk(test)
    ai.emulate_speech("what time is it")
    ai2 = Client(key='asdfasdf')
    ai2.talk('this is a false test')


"""
    Changelog- v.0.3.3
    - PEP-8
    - Added rest of Docstrings
    - Creating initial documentation using Sphinx


    Changelog- v.0.3.2
    - Better error response handling in _get_request() ( uses ast standard library module )
    - Optimized _get_xml() & _clear_xml() ( Thanks Zunair )
    - Fixed Get() function  ( typo in url )


    Changelog- v.0.3.1
    - Added XML support for access to Links UserVariables.xml file
    - Added more function wrappers - [Get("")], [Set("", "")]


    Changelog- v.0.2.1
    - Added APPDATA as default path to LINKS Install
    - Added 'Loquendo by Nuance' function wrapper
    - Added a bunch of other LINKS function as well ( check the README )
    - Adding get json response verification ( Adding type of response as parameter )
    - Added custom function parser



    :copyright: (c) 2016 by traBpUkciP.
    :license: BSD, see LICENSE for more details.
"""
