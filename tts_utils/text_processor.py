import re

def fix_upper_after_dot(text: str) -> str:
    return re.sub(
        r'\.\s+([A-ZÀ-Ỹ])',
        lambda m: '. ' + m.group(1).lower(),
        text
    )
import re

def process_text(text: str) -> str:
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)

    text = text.replace(",", ", ")
    text = text.replace(".", ".")   # nghỉ nhẹ
    text = text.replace(":", ": ")
    text = text.replace("!", "! .")
    text = text.replace('"', '" ')
    text = text.replace("?", "? .")
    text = text.replace("[", "[ ")
    text = text.replace("]", "] ")
    text = text.replace("\n", "\n")  # xuống dòng nghỉ vừa

    return text
