from pathlib import Path


class UiDesignFile:

    def __init__(self, file_name: str):
        super(UiDesignFile, self).__init__()
        self.path = Path(__file__).parent / file_name

    def __str__(self):
        return str(self.path)
