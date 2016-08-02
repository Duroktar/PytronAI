==========================================================
Pytron: A Python library for the LINKS Mark II A.I. v0.3.6
==========================================================

Interface with your Links AI and send commands from within your Python scripts. Send requests through Links Web Service
from any computer you want! Most of Links built in functions can be accessed by name with more being added all the time.
If you have any requests feel free to let me know on github under issues. You can report bugs there as well. Have fun!

  **Links: ( Free Windows AI Software )**
  http://mega-voice-command.com/

-Changelog at bottom of page under Updates-

Installation
============

Simple:

    install LINKS   ( http://mega-voice-command.com/ )
    
    pip install pytronlinks --upgrade

    `Full command list <http://pythonhosted.org/pytronlinks/genindex.html>`_ 
   

    
Example
=======

.. code-block:: python

    import pytronlinks as Pytron

    AI = Pytron.Client()

      """
      Optional client parameters-

        port: Port that links is listening on
        key: Links web key
        ip: ip of computer with links
        path: If you installed links in a different location,
                     point this to the Scripts folder( MUST BE RAW ) ie: (r'PATH')

      ex: AI = Pytron.Client(path='C:\\temp', ip='192.0.0.16', key='KEY123')
      """


Make Links speak!
=================

.. code-block:: python

    import pytronlinks as Pytron

    
    TEXT = ('MVC Rocks!')

    AI = Pytron.Client()
    AI.talk(TEXT)


Emulate speech to Links
=======================

Will call the command as if you had spoken to links directly.

.. code-block:: python

    import pytronlinks as Pytron

    
    TEXT = ('what is the weather like')

    AI = Pytron.Client()
    AI.emulate_speech(TEXT)
    AI.emulate_speech("stop talking")


Run custom action command
=========================

 Anything you can put in Links *Action* bar, you can put in here! See example.

.. code-block:: python

    import pytronlinks as Pytron


    AI = Pytron.Client()

    AI.custom(r'[Set("Last Subject", "pytron is the coolest")]')
    AI.custom(r'[Speak("[Get("Last Subject")]")]')


Get a list of all available commands
====================================

Returns a list of all callable commands.

*Coming soon*
'Use with write_commands_to_file to create a file containing all the available grammars to use as a reference.'

.. code-block:: python

    import pytronlinks as Pytron

    AI = Pytron.Client()

    grammars = AI.GetGrammarList()
    for commands in grammars:
        print commands


Get confirmation
================

Get confirmation before executing commands. Additional parameters not shown in example.

        :param trigger_var: Variable in UserVariable.xml to be used for Confirmation ( Default Variable used: "Answer" )
        :param confirm: Confirmation speech ( Ex: "Are you sure you want to play music?" )
        :param on_yes: Speech response if answer is "yes"
        :param on_no: Speech response if answer is "no"

.. code-block:: python

    import pytronlinks as Pytron  # Import Pytron


    AI = Pytron.Client()
    query = AI.listen('Pytron')  # Stars listening for input from Links

    if query == 'quit':
        break

    if query == "Play music":
        # Get confirmation returns True or False so it can be checked directly, like this..
        if AI.GetConfirmation(confirm="Do you want to play music?"):
            AI.emulate_speech('play music')


Put script into listen mode
===========================

Listens for user input by watching a variable in the UserVariables.xml file ( 'Pytron' by default ). The variable is
set using the [Set("variable", "value")] command in links. **See Example**

.. code-block:: python

    import pytronlinks
    """
            **Make a command in links social tab like this**
         Command: Links {speech=test_dictation}
         Response: [Set("Pytron", {speech})]
         Profile: Main

         And use the dictation in Pytron with the script below.. ( Ctrl-c to quit )
    """

    import pytronlinks as Pytron

    AI = Pytron.Client()

    def main():
        dictation = AI.listen()
        if dictation == 'quit':
            break
        else:
            AI.talk(dictation)

    try:
        while True:
            main()
    except KeyboardInterrupt:
        pass


Loquendo Function
=================

Sends a 'Loquendo by Nuance' speech command ( requires Nuance Loquendo voices )

        :param text: Text to be spoken ( with all the syntax they use, better make it raw, ie: r'text' )
        :param volume: Volume 0 - 100
        :param rate: Rate of speech 0 - 100 ( 50 is default )
        :param ai_name: Name of tts Voice ( case sensitive )

  Example:

.. code-block:: python

    import pytronlinks as Pytron

    ai.LoqSpeak("I am an example","100","50","Simon")]
    
Updates
=======

**New features!**
    **Changelog- v.0.3.6**
    - Tweaked CallCommand function. Now returns the response from Links.
    - Docstrings added for new functions
    - Shelved urllib in exchange for the Requests library
    - Add GetGrammarList function
    - write_commands_to_file function added ( Needs de-bugging )

    **Changelog- v.0.3.5**
    - Fixed Listen() function
    - Added more functions ( No docstrings yet, tsk tsk traBpUkciP)

    **Changelog- v.0.3.3**
      - PEP-8
      - Added rest of Docstrings
      - Created documentation using Sphinx

    **Changelog- v.0.3.2**
      - Better error response handling in _get_request() ( uses ast standard library module )
      - Optimized _get_xml() & _clear_xml() ( Thanks Zunair )
      - Fixed Get() function  ( typo in url )

    **Changelog- v.0.3.1**
      - Added XML support for access to Links UserVariables.xml file
      - Added more function wrappers - [Get("")], [Set("", "")]

    **Changelog- v.0.2.1**
      - Added APPDATA as default path to LINKS Install ( ai = pytronlinks.Client() )
      - Added 'Loquendo by Nuance' function wrapper
      - Added a bunch of other LINKS function as well ( check the README )
      - Adding get json response verification ( Adding type of response as parameter )
      - Added custom function parser



Authors
=======

Scott Doucet / aka: traBpUkciP / aka: Duroktar / `<https://github.com/Duroktar/>`__
