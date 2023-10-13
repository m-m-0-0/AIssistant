import os
import re
import urllib

def extract_tags(text : str) -> "dict[str, str, int, int]":
    """
    Extracts tags from a string.
    Tags are in the form of <tagname>content</tagname>
    Returns a dictionary of the form {tagname: {content, start, end}}
    """

    tags = {}
    tag_regex = re.compile(r"<(\w+)>(.*?)</\1>")
    
    for match in tag_regex.finditer(text):
        tag = match.group(1)
        content = match.group(2)
        start = match.start()
        end = match.end()
        tags[tag] = {"content": content, "start": start, "end": end}

    return tags