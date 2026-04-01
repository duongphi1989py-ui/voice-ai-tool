import re

def process_text(text: str) -> str:
    text = re.sub(r'\n+', '\n', text)

    text = text.replace(",", ", ")
    text = text.replace(".", ". ..")
    text = text.replace(":", ": ")
    text = text.replace("!", "! ")
    text = text.replace(""", "" ")
    text = text.replace("?", "? ")
    text = text.replace("[", "[ ")
    text = text.replace("]", "] ")

    text = text.replace("\n", "\n..")

    return text
