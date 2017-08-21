""" Date Handler Module
"""
import re
import dateparser
from ashaw_notes.plugins import base_plugin
import ashaw_notes.utils.configuration


class Plugin(base_plugin.Plugin):
    """Date Handler Plugin Class"""

    regex = re.compile(r'"([^"]*)"')

    def format_note_line(self, timestamp, note_line):
        """Allows enabled plugins to modify note display"""
        note_line = Plugin.regex.sub(
            r"<span style='color:#E6DB5A'>&quot;\1&quot;</span>",
            note_line)
        return note_line
