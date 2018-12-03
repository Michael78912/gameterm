"""shell.py- a shell that uses terminal."""

import inspect
import shlex
import enum
import contextlib
import threading
import sys
import argparse

import pygame as pg

import _command


class States(enum.Enum):
    INPUT = 0
    RUNNING = 1
    PROMPT = 2


HELP_SKELETON = """
{description}

{syntax}

{usage}
"""


class Shell:
    """adds some functionality to terminal."""

    surface = None
    help_enabled = True
    commands = []
    _events = []
    _state = States.PROMPT
    _dead = False

    def __init__(self, terminal, surface, pos=(0, 0), prompt="", command_prefix=""):
        """initiate self"""
        self.terminal = terminal
        self.prompt = prompt
        self.surface = surface
        self.pos = pos
        self.command_prefix = command_prefix

    def bind(self):
        """bind the terminal to sys.stdout/in"""
        sys.stdout = self.terminal
        sys.stdin = self.terminal
        sys.stderr = self.terminal

    def run_cmd(self, cmd, args):
        """attempt to run the command. if it does not exist, say it."""
        cmd = cmd.strip(self.command_prefix)
        if cmd == 'help' and self.help_enabled:
            self._help()
            return

        for command in self.commands:
            if command.function.__name__ == cmd:
                with contextlib.suppress(SystemExit):
                    ns = command.parser.parse_args(args)
                    command(**ns.__dict__)
                return

        print(cmd + ": command not found!")

    def kill(self):
        """stop mainloop"""
        self._dead = True
        self.terminal._dead = True

    def add_event(self, event):
        """add the event to queue"""
        self._events.append(event)
        self.terminal.event_queue.put(event)

    def mainloop(self, fps):
        """run main loop. update constantly, and
        constantly update.
        """
        main_thread = threading.main_thread() is threading.current_thread()
        self.terminal.do_update = main_thread
        clock = pg.time.Clock()
        while not self._dead:
            line = [i.strip() for i in shlex.split(input(self.prompt))]
            self.run_cmd(line[0], line[1:])
            clock.tick(fps)

            if main_thread:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        raise SystemExit
                    self.terminal.events.append(event)
                pg.display.flip()

        print("exiting mainloop")

    def command(self, func):
        """decorator function to act as a command, given to shell."""
        params = inspect.signature(func).parameters
        description_parts = func.__doc__.split("\n\n")

        parser = argparse.ArgumentParser(
            prog=func.__name__,
            description=description_parts[0],
            epilog=description_parts[1] if len(description_parts) > 1 else None,
        )

        for param in params.values():
            dic = {
                "annotation": param.annotation,
                "default": param.default,
                "name": param.name,
            }

            name = dic["name"]

            # for key, val in zip(dic.keys(), dic.values()):

            if dic["default"] != inspect._empty:
                parser.add_argument(
                    "--" + name,
                    nargs="?",
                    default=dic["default"],
                    help=dic["annotation"],
                    type=type(dic["default"]),
                )

            else:
                parser.add_argument(name, help=dic["annotation"])

        cmd = _command.Command(func, parser)
        self.commands.append(cmd)
        return cmd
    
    def threaded_update(self):
        """run this function if running terminal in a
        seperate thread. It helps do things like draw
        the cursor, etc...
        """
        self.terminal.draw_cursor()
        self.surface.blit(self.terminal.get_surf(), self.pos)
    
    def _help(self):
        """display help message"""
        if self.help_enabled:
            help_str = "Commands:\n\n"
            for cmd in self.commands:
                help_str += cmd.function.__name__ + "\n"
            help_str += "\n\nfor help on any individual command, type <cmd> -h."
        
            print(help_str)


def test2():
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
        # hold the shell open until enter is pressed
        input()
    if __name__ == '__main__':
        main()


if __name__ == "__main__":
    test2()