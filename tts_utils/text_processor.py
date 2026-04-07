import re
import random

# ================= CLEAN BASIC =================
def process_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = text.replace("\n", " <pause> ")
    text = text.replace('"', '')
    return text.strip()

# ================= FIX NUMBER =================
number_map = {
    "0": "không", "1": "một", "2": "hai", "3": "ba", "4": "bốn",
    "5": "năm", "6": "sáu", "7": "bảy", "8": "tám", "9": "chín"
}

def read_number(num_str):
    return " ".join(number_map.get(d, d) for d in num_str)

def fix_numbers_ultimate(text: str) -> str:
    def decimal_replace(match):
        return f"{match.group(1)} phẩy {read_number(match.group(2))}"

    text = re.sub(r'(\d+)\.(\d+)', decimal_replace, text)
    text = re.sub(r'(\d+)%', r'\1 phần trăm', text)

    def time_replace(match):
        return f"{int(match.group(1))} giờ {int(match.group(2))} phút"

    text = re.sub(r'(\d{1,2}):(\d{2})', time_replace, text)

    return text

# ================= FIX CASE =================
def fix_upper_after_dot(text: str) -> str:
    return re.sub(
        r'\.\s+([A-ZÀ-Ỹ])',
        lambda m: '. ' + m.group(1).lower(),
        text
    )

# ================= STORY RHYTHM =================
def story_engine(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text)

    result = []

    for s in sentences:
        s = s.strip()

        # hội thoại → mềm hơn
        if any(x in s for x in ["nói", "hỏi", "đáp"]):
            s += ", "

        # câu bình thường
        elif len(s) < 40:
            s += ", "

        # câu dài → nghỉ mạnh
        else:
            s += ". "

        result.append(s)

    return " ".join(result)

# ================= HUMANIZE =================
def humanize_text(text: str) -> str:
    words = text.split()
    result = []

    for i, w in enumerate(words):
        result.append(w)

        # pause nhẹ random
        if random.random() < 0.025:
            result.append(",")

        # pause theo keyword
        if w.lower() in ["nhưng", "và", "sau đó", "bỗng nhiên"]:
            result.append(",")

        # pause mạnh
        if w == "<pause>":
            result.append(".")
    
    return " ".join(result)

# ================= FINAL =================
def final_process(text: str) -> str:
    text = process_text(text)
    text = fix_numbers_ultimate(text)
    text = fix_upper_after_dot(text)
    text = story_engine(text)
    text = humanize_text(text)

    # clean cuối
    text = re.sub(r'\s+', ' ', text)
    text = text.replace(" ,", ",")
    text = text.replace(" .", ".")
    text = text.replace('"', " ")
    return text.strip()
