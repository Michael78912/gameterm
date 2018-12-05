"""class for a terminal, displayed as a surface.
"""
__all__ = ["Terminal"]

import sys
import time
import queue
import threading
import collections

import pygame as pg

from . import _terminal_state

_MS_WINDOWS = sys.platform == "win32"
_DEF_FONT = "Lucida Console" if _MS_WINDOWS else "monospace"

class _FakeEvent:
    """holds a fake event."""


# colour definitions.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 30 frames no there, 30 frames there.
CURSORFRAMES = 30



class Terminal:
    """gives the ability to view, handle, and run a terminal,
    as a surface.
    """

    do_update = False
    _state = _terminal_state.StageInfo()
    frames = 0
    event_queue = queue.Queue()
    dead = False
    rel_cursor = "_"
    last_input = ""
    cursor = rel_cursor
    surface = None
    pos = (0, 0)
    clock = pg.time.Clock()

    def read(self):
        pass
    
    def _readline_main(self):
        """read and return a single line, (running in main thread)"""
        finished = False

        while not finished or not self.dead:
            for ev in pg.event.get():
                finished = self.input(ev)

            self.update()
            self.surface.blit(self.get_surf(), self.pos)

            pg.display.flip()
            
            self.clock.tick(self.fps)



        return self.last_input

    def _readline_threaded(self):
        """read and return a single line."""
        finished = False

        while not finished:
            self.surface.blit(self.get_surf(), self.pos)
            finished = self.input(self.event_queue.get())
        
        return self.last_input
    
    def readline(self):
        """choose the right readline function"""
        return self._readline_main() if \
            threading.main_thread() == threading.current_thread() \
            else self._readline_threaded()
    
    def kill(self):
        """raise a systemexit in the current thread."""
        raise SystemExit


    # pylint: disable=too-many-arguments
    def __init__(
        self,
        surface,
        fps=60,
        bgcolour=BLACK,
        fgcolour=WHITE,
        font=_DEF_FONT,
        font_size=12,
        terminal_size=(500, 350),
        add_safe=True,
    ):
        """initiate instance of terminal"""
        self.fps = fps
        self.surface = surface
        self.bgcolour = bgcolour
        self._state.set_buffer(terminal_size[1] // font_size)
        self.fgcolour = fgcolour
        self.font = pg.font.SysFont(font, font_size)
        self.font_size = font_size
        self.terminal_size = terminal_size

        if add_safe:
            # add an extra amount onto the terminal, so characters dont get cut in half.
            self.terminal_size = (
                terminal_size[0],
                (terminal_size[1] % font_size) + terminal_size[1],
            )

    def write(self, words):
        """add the lines to final line."""
        lines = words.split("\n")
        self._state.prev_lines[-1] += lines[0]
        self._state.prev_lines += lines[1:]
        self._state.update()

    def flush(self):
        pass
        # self.surface.blit(self.get_surf(), (0, 0))

    def get_surf(self):
        """create and return a surface based on the past state."""

        surf = pg.surface.Surface(self.terminal_size)
        surf.fill(self.bgcolour)
        if len(self.bgcolour) == 4:
            surf.set_alpha(self.bgcolour[3])

        x = 0
        y = 0

        for i, line in enumerate(self._state.prev_lines):
            if i == len(self._state.prev_lines) - 1:
                # last line. add input to end of it.
                line += self._state.input
                line += self.cursor
            # print("rendering", line)
            try:
                fontsurf = self.font.render(line, False, self.fgcolour)
            except pg.error:
                continue
                with open('file.txt', 'w') as d:
                    d.write('continued')
            rect = fontsurf.get_rect()
            rect.topleft = (x, y)
            surf.blit(fontsurf, rect)
            # x += self.font_size
            y += self.font_size

        return surf

    def echo(self, line):
        """add another line to the state."""
        self.update()
        self._state.prev_lines.append(line)

    def draw_cursor(self):
        """draw the cursor to the screen, if in the correct frame."""
        self.frames += 1
        if self.frames > CURSORFRAMES:
            # now, draw the cursor.
            self.cursor = self.rel_cursor
        else:
            self.cursor = ""

        if self.frames >= CURSORFRAMES * 2:
            # reset cursor frames to 0.
            self.frames = 0

    def update(self):
        """update terminal and state."""
        self._state.update()
        self.draw_cursor()

    def addch(self, character):
        """add the character to the last line."""
        self._state.prev_lines[-1] += character

    def input(self, event):
        """check if event is a key down. if it is, add it to the last 
        line. if it is a return, then complete the line.
        """
        if event.type == pg.KEYDOWN:
            if event.unicode == "\r":
                # return key. finish line, and reset input.
                self._state.prev_lines[-1] += self._state.input
                self.last_input = self._state.input
                self._state.prev_lines.append("")
                self._state.input = ""
                return True

            elif event.unicode == "\b":
                
                # backspace. remove one character from end of string.
                self._state.input = self._state.input[:-1]

            else:
                self._state.input += event.unicode

        self.update()
        return False
