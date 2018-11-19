"""class for a terminal, displayed as a surface.
"""
__all__ = ['Terminal']

import os
import sys

import pygame

_MS_WINDOWS = sys.platform == 'win32'
_DEF_FONT = "Lucida Console" if _MS_WINDOWS else "monospace"

# colour definitions.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)



class Terminal:
    """gives the ability to view, handle, and run a terminal,
    as a surface.
    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 bgcolour=BLACK,
                 fgcolour=WHITE,
                 font=_DEF_FONT,
                 font_size=12,
                 terminal_size=(300, 200),
                 ):
        """initiate instance of terminal"""
        self.bgcolour = bgcolour
        self.fgcolour = fgcolour
        self.font = font
        self.font_size = font_size
        self.terminal_size = terminal_size

    
