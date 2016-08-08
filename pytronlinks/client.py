# -*- coding: UTF-8 -*-

"""
    Pytron - The MVC Links Interface
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Links for Python. Interact with Links from your scripts!

     http://mega-voice-command.com/


    :copyright: (c) 2016 by Scott Doucet / aka: traBpUkciP
    :license: BSD, see LICENSE for more details.
"""

import os
from time import sleep, time
import datetime
import xml.etree.ElementTree as ET
import ast
import requests


class Client(object):
    """ Main Pytron Client v.0.3.7

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
        :param path: If you installed links in a different location

        :Example:

            import pytronlinks

            ai = pytronlinks.Client()

        """

        self.path = path
        self.ip = ip
        self.port = port
        self.key = key


    def talk(self, text):
        """ Speaks through Links

        :param text: String to be spoken

        :Example:

            import pytronlinks


            ai = pytronlinks.Client()
            ai.talk("Links is the best!")

        """
        try:
            fcn = '[Speak("{}")]'.format(text)
            self._get_request(fcn)
        except Exception as e:
            print(e)
            return

    def emulate_speech(self, command):
        """ Sends an Emulate Speech Command -

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
        """ Insert your own Links Action Commands -
                Anything you can put in Links *Action* bar, you can put in here!
                This would be useful for new testing new Links functions that haven't
                made it to here yet. See example.

        :param string: See example..

        Example -

            import pytronlinks


            ai = pytronlinks.Client()

            ai.custom(r'[Set("Last Subject", "pytron is the coolest")]')
            ai.custom(r'[Speak("[Get("Last Subject")]")]')
        """
        self._get_request(string)
        return

    def GetConfirmation(self, trigger_var='Answer', confirm=None, on_yes=None, on_no=None, timeout=10):
        """

        :param trigger_var:
        :param confirm:
        :param on_yes:
        :param on_no:
        :param timeout:
        :return:
        """
        try:
            if not trigger_var:
                print("Need to select a trigger variable.")
                return
            if timeout > 60:
                timeout = 60
                print("Timeout set to max: 60 seconds.")
            if confirm:
                self.talk(confirm)
            for i in range(1, timeout):
                response = self._get_xml(trigger_var)
                if response == 'yes':
                    if on_yes:
                        self.talk(on_yes)
                    return True
                elif response == 'no':
                    if on_no:
                        self.talk(on_no)
                    return False
                else:
                    sleep(1)
                    # continue
            print("Confirmation timed out")
            return False
        except Exception as e:
            print(e)
            return False

    # Checks for any value in the UserVariables.xml file and returns it input when found. ( BLOCKING )
    def listen(self, var_name='Pytron', freq=0.2):
        """ Check out the example to see how you could use this. This is probably the most powerful feature.

        :param var_name: Name of the Variable you want to "listen" to. OPTIONAL. Defaults to 'Pytron'
        :param freq: Delay ( in seconds ) between checks. OPTIONAL. Defaults to 0.2 seconds



            ** Make a command in links social tab like this **
        Command: Links {speech=test_dictation}
        Response: [Set("Pytron", {speech})]
        Profile: Main

        Command: {answer=Answer}
        Response: [Set("Confirm", {{answer}})]
        Profile: Main

        And use the dictation in Pytron with the script below.. ( Ctrl-c to quit )
            v        v         v         v         v

        :Example:

            import pytronlinks

            ai = pytronlinks.Client()

            def main():

                dictation = ai.listen()
                if not dictation:
                    break

                confirm = ai.GetConfirmation(confirm='Did you say - {}?').format(dictation)
                if not confirm:
                    break

                results = some_crazy_function(dictation)
                if not results:
                    break

                ai.talk(results)

            try:
                while True:
                    main()
            except KeyboardInterrupt:
                pass
        """
        try:
            self._clear_xml(var_name)
            print("Listening..")
            while True:
                x = self._get_xml(var_name)
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
            print("Exception in Loquendo function."
                  "It's quite possible that something happened."
                  "Because it works fine on my computer..")
            return

    def Get(self, var_name):
        """ Gets a variable saved in the '\\LINKS\\Customization\\XML\\UserVariables.xml' file.

        :param var_name: Name of variable to get the value of
        :return: Returns the value of the variable
        """
        try:
            fcn = '[Get("{}")]'.format(var_name)
            self._get_request(fcn)
            return self._get_xml(var_name)
        except Exception as e:
            print(e)
            print("Exception in Get function."
                  "Gonna need coffee for this one.")
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

    def GetWord(self, wordlist, grammar, column):
        """ Returns wordlist items by grammar (line) and column name

        :param wordlist: File name of wordlist ( file type not needed )
        :param grammar: Basically the line index. ( ie: first column )
        :param column: Column to return value from ( name or index )
        :return: Returns True or False
        """
        try:
            fcn = '[GetWord("{}", "{}", "{}")]'.format(wordlist, grammar, column)
            x = self._get_request(fcn)
            return x
        except Exception as e:
            print(e)
            print("Exception in Get Word function.")
            return

    def CallCommand(self, command):
        """ Calls any non-dynamic commands and returns the response from links
        :param command: Any command that doesn't contain a wordlist or function
        :return: Returns the response from Links as a string

        """
        try:
            fcn = '[CallCommand("{}")]'.format(command)
            result = self._get_request(fcn)
            return result
        except Exception as e:
            print(e)
            print("Exception in Call Command function."
                  "You got something on your shirt there.. /SLAP")
            return

    def GetGrammarList(self, data_type="XML"):
        """ Returns a list of all callable commands. Use with write_commands_to_file to create a file containing
        all the available grammars to use as a reference.

        :param data_type:
        :return:
        """
        try:
            ip = self.ip
            port = self.port
            key = self.key
            d_type = data_type

            action = '?action=[GetGrammarList("{}")]'.format(d_type).upper()
            output = '&output={}'.format(d_type).lower()
            request = '&request=disable_recurse'
            url = 'http://{}:{}/{}{}{}&key={}'.format(ip, port, action, output, request, key)

            r = requests.get(url)
            x = list(r.iter_lines())
            root_ = ET.fromstringlist(x[4:])
            response = root_.find('response')
            xml = self.strip_non_ascii(response.text)
            gram = ET.fromstring(xml.encode('utf-16-be'))
            grammars = gram.findall('grammar')
            return_list = []

            for i in grammars:
                section = i.find('Name')
                commands = i.findall('Commands')
                enabled = i.find('Enabled')
                loaded = i.find('Loaded')
                DebugShowPhrases = i.find('DebugShowPhrases')
                priority = i.find('Priority')
                name = section.text
                name_len = len(name)
                underscore = "=" * name_len

                if str(enabled.text) == 'true':
                    enabled = "Enabled"
                    # print enabled
                else:
                    enabled = "Disabled"
                    # print enabled

                if str(loaded.text) == 'true':
                    loaded = "Loaded"
                    # print loaded
                else:
                    loaded = "Not loaded"
                    # print loaded
                enabled = "*" + enabled + "*"
                loaded = "*" + loaded + "*"
                return_list.append(name)
                return_list.append(underscore)
                return_list.append(enabled)
                return_list.append(loaded)
                return_list.append('\n')
                for each in commands:
                    return_list.append(each.text)

                return_list.append('\n \n')

            return return_list
        except Exception as e:
            print(e)
            print("Exception in Get Grammar List function.")
            return False


    def SayAs(self, before, data, content, after=""):
        """ This function is only for speech. Will speak the appropriate way for the given data type. ( See example )

        :param before: In the example, the before string is "The phone number is" ( can be blank )
        :param after: In the example, the after string is "how cool is that?" ( defaults to blank )
        :param data: Data to be spoken as
        :param content: see https://msdn.microsoft.com/en-us/library/system.speech.synthesis.sayas(v=vs.110).aspx )

        Example:

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
            fcn = '[SpeakEx("{}", "{}", "{}", "{}", "{}", "{}")]'.format(phrase, name, vol, rate,
                                                                         delay, sys_or_voice_vol)
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
            url = 'http://{}:{}/?action={}&key={}&output=json'.format(ip, port, fcn, key)
            r = requests.get(url)
            if r.status_code and r.status_code == 200:
                x = list(r.iter_lines())[3]
                j = ast.literal_eval(x)
                # print(j)
                result = j['response']
                # print result
                err = (j['error'])
                if len(err) > 0:
                    print("v" * 20)
                    z = err + "\n" + result
                    print(z)
                    print("^" * 20)
                    print("\n")
                    return False
                else:
                    # print(result)
                    return result
            elif r.status_code:
                err = 'Error {}'.format(r.status_code)
                print(err)
                return err
            else:
                print("Something went terribly wrong.....")
                return False
        except Exception as e:
            print(e)
            print("Exception in _get_request function. \n"
                  "***Check your ip, port and key settings!*** \n"
                  "Also, your shoes are untied..")
            return False

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

    def write_commands_to_file(self, commands):
        """ Writes a list of commands to a file in rst format.

        :param commands: List of commands returned bt GetGrammarList function
        :return: Returns True or Exceptions
        """
        try:
            data = commands
            print type(data)
            with open(self._SCRIPTS_PATH + r'\command_list.txt', 'w') as f:
                f.writelines(data)
                f.close()
                return True
        except Exception as e:
            return e

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


# Used for testing
if __name__ == '__main__':
    ai = Client()
    ai.talk('Hello')
    # print(ai.GetWord("test_greetings", "hello", "converted value"))
    # print(ai.GetWord("RSSFeeds", "CNN", "url"))
    # print(ai.GetWord("RSSFeeds", "New York Times", "url"))
    # ai.Set('Pytron', 'This is the first test')
    # test = ai.Get('Pytron')
    # print("This is the first test: ", test)
    # ai.talk(test)
    # ai.Set('Pytron', 'This is the second test')
    # test = ai.Get('Pytron')
    # print("This is the second test: ", test)
    # ai.talk(test)
    # temp = ai.CallCommand("whats the temperature")
    # print(temp)
    # test = ai.CallCommand("Greetings")
    # print test
    # ai.emulate_speech("open windows explorer")
    # print(ai.CallCommand("what time is it"))
    # confirm = ai.GetConfirmation(confirm='Say yes or no to continue', on_yes="You said yes", on_no="You said no")
    # if confirm:
    #     print("WORKS!")
    # if not confirm:
    #     print("NOT CONFIRM!")
    # if confirm is None:
    #     print("CONFIRM IS NONE!")
    # print("Confirm :", confirm)
    # x = ai.GetGrammarList()
    # ai.write_commands_to_file(x)


"""
    Changelog- v.0.3.7
    - Fixed error on Client initialization


    Changelog- v.0.3.6
    - Tweaked CallCommand function. Now returns the response from Links.
    - Docstrings added for new functions
    - Shelved urllib in exchange for the Requests library
    - Add GetGrammarList function
    - write_commands_to_file function added ( Needs de-bugging )


    Changelog- v.0.3.5
    - Fixed Listen() function
    - Added more functions ( No docstrings yet, tsk tsk traBpUkciP)


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



    :copyright: (c) 2016 by Scott Doucet / aka: traBpUkciP.
    :license: BSD, see LICENSE for more details.
"""
