=============
pytron v0.3.2
=============

Interface with your Links AI and send commands from within your Python scripts. Most of Links built in functions
can be accessed by name with more being added all the time. If you have any requests feel free to let me know,
e-mail is down below. Thanks!

  Links: ( Free Windows AI Software )
  http://mega-voice-command.com/

  ** Changelog at bottom of page under Updates **

Installation
============

Simple:

    pip install pytronlinks --upgrade

    install LINKS   ( http://mega-voice-command.com/ )


Example
=======

.. code-block:: python

    import pytronlinks

    ai = pytronlinks.Client()

      """
      Optional client parameters-

        port: Port that links is listening on
        key: Links web key
        ip: ip of computer with links
        path: If you installed links in a different location,
                     point this to the Scripts folder( MUST BE RAW ) ie: (r'PATH')

      ex: ai = pytronlinks.Client(path='C:\\temp', ip='192.0.0.16', key='KEY123')
      """


Make Links speak!
=================

.. code-block:: python

    import pytronlinks

    
    TEXT = ('MVC Rocks!')

    ai = pytronlinks.Client()
    ai.talk(TEXT)


Emulate speech to Links
=======================

.. code-block:: python

    import pytronlinks

    
    TEXT = ('what is the weather like')

    ai = pytronlinks.Client()
    ai.emulate_speech(TEXT)

        Will call the command as if you had spoken to links directly


Run custom action command
=========================

 Anything you can put in Links *Action* bar, you can put in here! See example.

.. code-block:: python

    import pytronlinks


    ai = pytronlinks.Client()

    ai.custom(r'[Set("Last Subject", "pytron is the coolest")]')
    ai.custom(r'[Speak("[Get("Last Subject")]")]')


Put script into listen mode
===========================

.. code-block:: python

    import pytronlinks
    """
            ** Make a command in links social tab like this **
         Command: Links {speech=test_dictation}
         Response: [Set("Pytron", {speech})]
         Profile: Main

         And use the dictation in Pytron with the script below.. ( Ctrl-c to quit )
    """

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


Loquendo Function
=================

Sends a 'Loquendo by Nuance' speech command ( requires Nuance Loquendo voices )

        :param text: Text to be spoken ( with all the syntax they use, better make it raw, ie: r'text' )
        :param volume: Volume 0 - 100
        :param rate: Unsure of rate   ( needs testing )
        :param ai_name: Name of tts Voice ( case sensitive )

  Example:

.. code-block:: python

    import pytronlinks

    ai = pytronlinks.Client()
    ai.LoqSpeak("I am an example","100","50","Simon")]
    
Updates
=======

New features! -
    Changelog- v.0.3.1
    - Added XML support for access to Links UserVariables.xml file
    - Added more function wrappers - [Get("")], [Set("", "")]

    Changelog- v.0.2.1
    - Added APPDATA as default path to LINKS Install ( ai = pytronlinks.Client() )
    - Added 'Loquendo by Nuance' function wrapper
    - Added a bunch of other LINKS function as well ( check the README )
    - Adding get json response verification ( Adding type of response as parameter )
    - Added custom function parser



Authors
=======

traBpUkciP / `<https://github.com/Duroktar/>`__
