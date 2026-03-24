import re

def auto_pause(text):
    text = text.replace("\n", " ... ")
    text = text.replace("~", " ... ")

    text = re.sub(r"\.", ". ... ", text)
    text = re.sub(r",", ", ... ", text)
    text = re.sub(r"!", "! ... ", text)
    text = re.sub(r"\?", "? ... ", text)

    return text
