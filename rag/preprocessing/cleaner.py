"""
Text Cleaner module for preprocessing text content prior to chunking & embedding.
"""

import re
class TextCleaner:
    """
    Cleans and normalizes raw markdown and text strings.
    """

    def __init__(self, remove_markdown_syntax: bool = False, lower_case: bool = False):
        self.remove_markdown_syntax = remove_markdown_syntax
        self.lower_case = lower_case

    def clean(self, text: str) -> str:
        """
        Cleans input text by removing extra spaces, linebreaks, and optionally markdown headers.
        """
        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r\n", "\n")

        if self.remove_markdown_syntax:
            # Remove Markdown headers (#, ##, etc)
            text = re.sub(r"^#+\s+", "", text, flags=re.MULTILINE)
            # Remove Markdown bold/italic syntax
            text = re.sub(r"[\*_]{1,3}([^\*_]+)[\*_]{1,3}", r"\1", text)
            # Remove inline links [text](url) -> text
            text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

        # Normalize multiple spaces and blank lines
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        if self.lower_case:
            text = text.lower()

        return text.strip()
