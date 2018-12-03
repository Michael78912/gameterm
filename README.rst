====================================
gameterm- terminal for pygame_ games
====================================
.. _pygame: https://pygame.org

.. image:: https://raw.githubusercontent.com/Michael78912/gameterm/master/screenshots/test_shell_bg.PNG

.. contents ::

*****
About
*****

- gameterm is a minimal package, designed for `Stickman's New World <https://github.com/Michael78912/SMNW>`_.
it will have the abilty to return a surface of the terminal in its proper state. more info will come as 
development continues!

*****
Usage
*****

there are two main parts to gameterm, ``terminal`` and ``shell``. terminal is the base window itself, or part of 
the window, where the text is actually displayed, and commands are entered. shell is a class bound to a terminal,
used to give the terminal some functionality.

gameterm is desinged to work well with python's ``threading`` module, to allow functions like ``input()`` not
to block the functionality of your game, or whatever you are doing.

gameterm.terminal.Terminal
==========================

methods
*******

- ``read()``: not implemented. will do nothing.
- ``readline()``: read and return a single line. will act as a blocking function, until the user hits return.
- ``write(text)``: add the text to the last line. split on newlines.
- ``flush()``: do nothing. (implemented for use as a file stream)
- ``get_surf()``: build and return a ``pygame.Surface`` object, representing the terminal.
- ``echo(line)``: add line to the lines in the terminal.
- ``draw_cursor()``: check if the cursor should be on or off. if it should be on, make sure it is rendered.
- ``addch(char)``: add the character to the end of last line.
- ``input(event)``: take the event object. if it is KEYDOWN, add the character to the last line.

constructor
***********

.. code-block:: python

    Terminal(surface,
              fps=60,                     # run at this FPS if in main thread
              bgcolour=BLACK,             # (0, 0, 0)
              fgcolour=WHITE,             # (255, 255, 255)
              font=_DEF_FONT,             # monospace on *nix, Lucida Console on Windows
              font_size=12,               # font size (pixels)
              terminal_size=(500, 350),   # terminal size (pixels)
              add_safe=True,              # add a safe amount of height to the terminal in proportion to the font size
          )





the following is a basic example of terminal's use, without threading.

.. code-block:: python

    import sys

    import pygame

    import terminal

    def main():
        pygame.init()
        display = pygame.display.set_mode((500, 350))

        term = terminal.Terminal(display)

        sys.stdout = term
        sys.stdin = term

        # this will block, as term.readline will run until complete
        print(input())
        # hold the terminal open until enter is pressed
        input()


    if __name__ == '__main__':
        main()


gameterm.shell.Shell
====================

methods
*******

use whenever
""""""""""""

- ``bind()``: set sys.stdout, sys.stdin and sys.stdout to the current terminal.
- ``run_cmd(cmd, args)``: run the command, if found, with arguments of args.
- ``mainloop(fps)``: run a mainloop constantly, updating terminal, and running commands.
- ``disable_help()``: disable the "help" command of the shell.

use when multithreading
"""""""""""""""""""""""

- ``kill()``: stop the mainloop from running.
- ``add_event(event)``: add the event to self, and terminal's queue.
- ``command()``: use as a decorator, see commands_
- ``threaded_update()``: use every frame to make sure the cursor is drawn correctly


constructor
***********

.. code-block:: python

    Shell(terminal,              # terminal object to be used
          surface,               # main display surface
          pos=(0, 0),            # position (top left) where terminal will be displayed 
          prompt="",             # prompt of the command
          command_prefix=""      # prefix used when calling command
    )

commands
========

a command is created through the decorator ``Shell.command``. it can act like any normal function.

a command can have type annotations, defaults, and a docstring, which will be parsed, in order to
make a good command parser (through argparse), and run it through that.

for example (from tests/test_shell.py):

.. code-block:: python
    surf = pygame.display.set_mode((500, 350))
    shell = Shell(Terminal(s), s, prompt="> ")

    @shell.command
    def add(num1: "first number", num2: "second number"):
        """
        add two numbers.
        
        note: if num1 is divisible by 8, it will say "howdy" instead.
        """

        if float(num1) % 8 == 0:
            # divisible by 8.
            print('howdy')
        else:
            print(float(num1) + float(num2))

you could now call ``shell.mainloop()`` and it would run as expected.

the output of ``howdy -h`` is below:

.. code-block ::

    usage: add [-h] num1 num2

    add two numbers.

    positional arguments:
      num1        first number
      num2        second number

    optional arguments:
      -h, --help  show this help message and exit

    note: if num1 is divisible by 8, it will say "howdy" instead.

Use with threading
==================

the following is the entire example from tests/test_shell.py. It demonstrates use of a shell with threading,
allowing you to run the shell at the same time as your game.


.. code-block:: python

    """test the shell module using a thread."""

    import sys
    import os
    import threading
    # insert parent directory into PYTHONPATH
    sys.path.append(os.path.realpath('..\\gameterm'))
    print(sys.path)

    import pygame as pg

    import terminal
    from shell import Shell


    def test_shell():
        """create and run shell, using three really stupid commands."""
        # initiate pygame, create shell object
        pg.init()
        display = pg.display.set_mode((500, 350))
        shell = Shell(terminal.Terminal(display), display, prompt="> ")

        # make sys.stdout, err, and in the terminal
        # shell.bind()

        # start the thread for handling the shell.
        threading.Thread(target=lambda: shell.mainloop(60), daemon=True).start()

        clock = pg.time.Clock()
        fps = 60

        @shell.command
        def say_hi(hello: "say hello instead of hi" = False):
            """say hi.
            if hello is true, say hello instead.
            """
            print('hello' if hello else 'hi')
        

        @shell.command
        def add(num1: "first number", num2: "second number"):
            """
            add two numbers.

            note: if num1 is divisible by 8, it will say "howdy" instead.
            """

            if int(num1) % 8 == 0:
                # divisible by 8.
                print('howdy')
            else:
                print(float(num1) + float(num2))
        
        @shell.command
        def echo():
            """ask user for input, and print it once enter has been pressed."""
            print(input())


        while True:
            for event in pg.event.get():
                # add all events
                shell.add_event(event)
                if event.type == pg.QUIT:
                    raise SystemExit

            shell.threaded_update()
            pg.display.update()
            clock.tick(fps)

    if __name__ == '__main__':
        test_shell()

contributing
============

If you wish to contribute, please feel free! Please Fork_ it, then create a `Pull Request`_!

.. _Fork: https://github.com/michael78912/gameterm/fork

.. _`Pull Request`: https://github.com/Michael78912/gameterm/compare
            









