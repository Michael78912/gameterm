"""this class can keep track of the previous command run,
buffer size to remember, and everything internal
(or, should I say, interminal) about the terminal. :)
"""

# amount of lines to hold in memory
# _BUFFER_SIZE = 1000


class StageInfo:
    """holds info about the terminal."""
    # buf_size = _BUFFER_SIZE
    prev_lines = [""]
    buf_size = 0
    input = ""
    last_command = None

    def set_buffer(self, lines):
        """set the amount of lines the terminal will display."""
        self.buf_size = lines

    def update(self):
        """check to see if the lines need to be truncated,
        and check for any line breaks.
        """
        if len(self.prev_lines) > self.buf_size:
            # need to remove all lines prior to self.buf_size
            # print('cutting lines to', self.prev_lines[-self.buf_size:])
            self.prev_lines = self.prev_lines[-self.buf_size:]
