from AIssistant import Plugin
import os

class OpenPlugin(Plugin):
    def __init__(self):
        command = "open"
        arguments = ["file/program name"]
        description = "Open a file or program"
        examples = ["open notepad"]
        super(OpenPlugin, self).__init__(command, arguments, description, examples=examples)

    def execute(self, *args, **kwargs):
        os.system("start " + args[0])

