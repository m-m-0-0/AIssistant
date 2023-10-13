from AIssistant import Plugin
import os

class NavigatePlugin(Plugin):
    def __init__(self):
        command = "navigate"
        arguments = ["url"]
        description = "(useful for specific searches too eg. youtube or open various websites. you can also use this with other protocols eg. steam:// or spotify:// or discord:// and many more)"
        examples = ["navigate https://www.youtube.com/watch?v=dQw4w9WgXcQ", "navigate spotify://search/porter%20robinson", "navigate https://www.google.com/search?q=how+to+make+a+discord+bot"]
        super(NavigatePlugin, self).__init__(command, arguments, description, examples=examples)

    def execute(self, *args, **kwargs):
        os.system("start " + args[0])