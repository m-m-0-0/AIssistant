class Plugin:
    def __init__(self, command, arguments, description, examples=None, remove_args_from_input=True):
        self.command = command
        self.arguments = arguments
        self.description = description
        self.examples = examples
        self.remove_args_from_input = remove_args_from_input

    def execute(self, *args, **kwargs):
        raise NotImplementedError("Plugins must implement the execute method.")
    
    def format_prompt(self, n):
        return f"{n}. {self.command} {''.join('<'+arg+'>' for arg in self.arguments)}: {self.description}" + ("" if self.examples is None else f"\n\tExamples: {' '.join(f'<command>{example}</command>' for example in self.examples)}")