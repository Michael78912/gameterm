====================================
gameterm- terminal for pygame_ games
====================================
.. _pygame: https://pygame.org

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

terminal
========

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

a single threaded example will work just like a normal terminal window. The real usefulness comes with
a couple threads.



