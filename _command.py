"""internal class of Shell to replicate a command."""


class Command:
    def __init__(self, func, parser):
        """initiate self."""
        self.parser = parser
        self.function = func
        
    def __call__(self, *args, **kwargs):
        """run self.function."""
        self.function(*args, **kwargs)


