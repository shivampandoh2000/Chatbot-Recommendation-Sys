"""
Statement pre-processors.
"""


def clean_whitespace(statement):
    """
    Remove any consecutive whitespace characters from the statement text.
    """
    import re

    # Replace linebreaks and tabs with spaces
    statement.Solution = statement.Solution.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    # Remove any leeding or trailing whitespace
    statement.Solution = statement.Solution.strip()

    # Remove consecutive spaces
    statement.Solution = re.sub(' +', ' ', statement.Solution)

    return statement


def unescape_html(statement):
    """
    Convert escaped html characters into unescaped html characters.
    For example: "&lt;b&gt;" becomes "<b>".
    """
    import html

    statement.Solution = html.unescape(statement.Solution)

    return statement


def convert_to_ascii(statement):
    """
    Converts unicode characters to ASCII character equivalents.
    For example: "på fédéral" becomes "pa federal".
    """
    import unicodedata

    text = unicodedata.normalize('NFKD', statement.Solution)
    text = text.encode('ascii', 'ignore').decode('utf-8')

    statement.Solution = str(text)
    return statement
