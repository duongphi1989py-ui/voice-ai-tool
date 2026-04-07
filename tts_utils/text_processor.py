import re
import random

# ================= FIX VIẾT HOA SAU DẤU . =================
def fix_upper_after_dot(text: str) -> str:
    return re.sub(
        r'\.\s+([A-ZÀ-Ỹ])',
        lambda m: '. ' + m.group(1).lower(),
        text
    )

# ================= MAP SỐ =================
number_map = {
    "0": "không", "1": "một", "2": "hai", "3": "ba", "4": "bốn",
    "5": "năm", "6": "sáu", "7": "bảy", "8": "tám", "9": "chín"
}

def read_number(num_str):
    return " ".join(number_map.get(d, d) for d in num_str)

# ================= FIX SỐ ULTIMATE =================
def fix_numbers_ultimate(text: str) -> str:

    # ===== 1. SỐ THẬP PHÂN (12.45 → 12 phẩy bốn năm) =====
    def decimal_replace(match):
        integer = match.group(1)
        decimal = match.group(2)
        return f"{int(integer)} phẩy {read_number(decimal)}"

    text = re.sub(r'(\d+)\.(\d+)', decimal_replace, text)

    # ===== 2. PHẦN TRĂM (50% → 50 phần trăm) =====
    text = re.sub(r'(\d+)\s*%', r'\1 phần trăm', text)

    # ===== 3. GIỜ (09:05 → 9 giờ 5 phút) =====
    def time_replace(match):
        h = int(match.group(1))
        m = int(match.group(2))
        return f"{h} giờ {m} phút"

    text = re.sub(r'(\d{1,2}):(\d{2})', time_replace, text)

    return text

# ================= SOFTEN DẤU . =================
def soften_dots(text):
    sentences = text.split(". ")
    result = []

    for i, s in enumerate(sentences):
        if i < len(sentences) - 1:
            # 70% thành dấu phẩy (đỡ khựng)
            if random.random() < 0.7:
                result.append(s + ", ")
            else:
                result.append(s + ". ")
        else:
            result.append(s)

    return "".join(result)

# ================= PROCESS TEXT =================
def process_text(text: str) -> str:
    # bỏ khoảng trắng dư
    text = re.sub(r'\s+', ' ', text)

    # xuống dòng
    text = text.replace("\n", ". ")

    # fix dấu cơ bản
    text = text.replace(",", ", ")
    text = text.replace(":", ": ")
    text = text.replace("!", ", ")
    text = text.replace("?", ", ")

    # bỏ dấu " gây khựng → đổi thành ,
    text = text.replace('"', ' ')

    return text

# ================= STORY ENGINE =================
def story_engine(text):
    text = text.strip()

    # nhịp nhẹ tự nhiên
    text = re.sub(r",", ", ", text)
    text = re.sub(r"!", "! ", text)

    return text
def smooth_text(text):
    # giảm cụm gây khựng
    text = re.sub(r'\s*,\s*', ', ', text)
    text = re.sub(r'\s+', ' ', text)

    # thêm nhịp nhẹ kiểu người
    words = text.split()
    result = []

    for i, w in enumerate(words):
        result.append(w)

        # random nghỉ nhẹ
        if random.random() < 0.03:
            result.append(",")

    return " ".join(result)
