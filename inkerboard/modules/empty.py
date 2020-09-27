from inkerboard.modules.module import Module


class Empty(Module):
    def __init__(self):
        super().__init__(background=self.WHITE)

    def render(self):
        return self.module
