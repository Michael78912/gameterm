"""this class can keep track of the previous command run,
buffer size to remember, and everything internal
(or, should I say, interminal) about the terminal. :)
"""

# amount of lines to hold in memory
_BUFFER_SIZE = 1000

class StageInfo:
    """holds info about the terminal."""
    buf_size = _BUFFER_SIZE
    prev_lines = []
    last_command = None

    