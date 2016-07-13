======
pytron
======

Interface with your Links AI and send commands from within your Python scripts.

  http://mega-voice-command.com/


Installation
============

Simple:

    pip install pytronlinks

    install LINKS   ( http://mega-voice-command.com/ )


Example
=======

 BE SURE TO APPEND THE ACTUAL PATH WITH r TO MAKE IT A RAW STRING (ex: r'C:\Path\To\Links\Scripts')


.. code-block:: python

    import pytronlinks

    path = (r'C:\users\default\AppData\Roaming\LINKS\Customization\Scripts')  # The path to Links install

    ai = pytronlinks.Client(path)


Make Links speak!
=================

.. code-block:: python

    import pytronlinks

    PATH = (r'C:\users\default\AppData\Roaming\LINKS\Customization\Scripts')
    TEXT = ('MVC Rocks!')

    ai = pytronlinks.Client(PATH)
    ai.talk(TEXT)


Emulate speech to Links
==========================

.. code-block:: python

    import pytronlinks

    PATH = (r'C:\users\default\AppData\Roaming\LINKS\Customization\Scripts')
    TEXT = ('what is the weather like')

    ai = pytronlinks.Client(PATH)
    ai.emulate_speech(TEXT)

        Will call the command as if you had spoken to links directly


Put script into listen mode
==========================

.. code-block:: python

    import pytronlinks
    """
        To get dictation from Links into the dictation.txt file for pytron
        to do something with, make a command in Links like this -

          Command: pytron {speech=test_dictation}
          Response:
          Action: CMD /m /c "echo {speech} > \dictation.txt"
    """

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


Authors
=======

traBpUkciP / `<https://github.com/Duroktar/>`__
