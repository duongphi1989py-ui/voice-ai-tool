import re

# ================= BASIC NUM =================
nums = ["không","một","hai","ba","bốn","năm","sáu","bảy","tám","chín"]

# ================= READ NUMBER =================
def read_number(n):
    n = int(n)

    if n < 10:
        return nums[n]

    if n < 20:
        if n == 15:
            return "mười lăm"
        return "mười " + nums[n % 10]

    if n < 100:
        tens = n // 10
        unit = n % 10
        result = nums[tens] + " mươi"

        if unit == 1:
            result += " mốt"
        elif unit == 5:
            result += " lăm"
        elif unit != 0:
            result += " " + nums[unit]

        return result

    if n < 1000:
        hundred = n // 100
        rest = n % 100
        result = nums[hundred] + " trăm"

        if rest == 0:
            return result

        if rest < 10:
            return result + " linh " + nums[rest]

        return result + " " + read_number(rest)

    if n < 1_000_000:
        thousands = n // 1000
        rest = n % 1000

        result = read_number(thousands) + " nghìn"

        if rest == 0:
            return result

        if rest < 100:
            return result + " không trăm " + read_number(rest)

        return result + " " + read_number(rest)

    if n < 1_000_000_000:
        millions = n // 1_000_000
        rest = n % 1_000_000

        result = read_number(millions) + " triệu"

        if rest == 0:
            return result

        return result + " " + read_number(rest)

    return str(n)

# ================= SPECIAL READ =================
def read_decimal(match):
    integer = match.group(1)
    decimal = match.group(2)
    int_part = read_number(integer)
    dec_part = " ".join(nums[int(d)] for d in decimal)
    return f"{int_part} phẩy {dec_part}"

def read_time(match):
    h = int(match.group(1))
    m = int(match.group(2))
    return f"{read_number(h)} giờ {read_number(m)}"

def read_percent(match):
    return f"{read_number(match.group(1))} phần trăm"

def read_money(match):
    return f"{read_number(match.group(1))} đồng"

def read_short_money(match):
    n = int(match.group(1))
    unit = match.group(2)
    if unit == "k":
        return f"{read_number(n)} nghìn"
    if unit == "tr":
        return f"{read_number(n)} triệu"

def read_unit(match):
    number = match.group(1)
    unit = match.group(2)

    unit_map = {
        "km": "ki lô mét",
        "kg": "ki lô gam",
        "m": "mét"
    }

    return f"{read_number(number)} {unit_map.get(unit, unit)}"

# ================= CLEAN TEXT =================
def process_text(text: str) -> str:
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)

    text = text.replace(",", ", ")
    text = text.replace(":", ": ")
    text = text.replace("!", "! ")
    text = text.replace("?", "? ")

    # 🔥 giảm độ khựng dấu chấm
    text = text.replace(". ", ". ")

    # thay " thành nghỉ nhẹ
    text = text.replace('"', ", ")

    return text.strip()

# ================= FIX HOA SAU DẤU =================
def fix_upper_after_dot(text: str) -> str:
    return re.sub(
        r'([\.!\?]\s+)([A-ZÀ-Ỹ])',
        lambda m: m.group(1) + m.group(2).lower(),
        text
    )

# ================= MAIN PROCESS =================
# ================= FIX NUMBER ULTIMATE 2 =================
def fix_numbers_level_max(text: str) -> str:

    # ================= PROTECT DECIMAL =================
    decimals = {}

    def protect_decimal(match):
        key = f"__DEC_{len(decimals)}__"
        decimals[key] = match.group()
        return key

    text = re.sub(r'\b\d+\.\d+\b', protect_decimal, text)

    # ================= TIME =================
    text = re.sub(r'\b(\d{1,2})[:h](\d{1,2})\b',
                  lambda m: f"{read_number(m.group(1))} giờ {read_number(m.group(2))}", text)

    # ================= % =================
    text = re.sub(r'\b(\d+)%',
                  lambda m: f"{read_number(m.group(1))} phần trăm", text)

    # ================= MONEY =================
    text = re.sub(r'\b(\d+)[\.,]?\d*đ',
                  lambda m: f"{read_number(m.group(1))} đồng", text)

    # ================= k, tr =================
    text = re.sub(r'\b(\d+)(k|tr)\b',
                  lambda m: f"{read_number(m.group(1))} nghìn" if m.group(2) == "k"
                  else f"{read_number(m.group(1))} triệu", text)

    # ================= 1,234 =================
    text = re.sub(r'\b\d{1,3}(,\d{3})+\b',
                  lambda m: read_number(m.group().replace(",", "")), text)

    # ================= INTEGER =================
    text = re.sub(r'\b\d+\b',
                  lambda m: read_number(m.group()), text)

    # ================= RESTORE DECIMAL =================
    def read_decimal_safe(s):
        parts = s.split(".")
        int_part = read_number(parts[0])
        dec_part = " ".join(nums[int(d)] for d in parts[1])
        return f"{int_part} phẩy {dec_part}"

    for key, val in decimals.items():
        text = text.replace(key, read_decimal_safe(val))

    return text
# ================= PROTECT DECIMAL =================
def protect_decimal(text: str):
    decimals = {}

    def replacer(match):
        key = f"__DEC_{len(decimals)}__"
        decimals[key] = match.group()
        return key

    text = re.sub(r'\b\d+\.\d+\b', replacer, text)
    return text, decimals


def restore_decimal(text: str, decimals: dict):
    for key, val in decimals.items():
        parts = val.split(".")
        int_part = read_number(parts[0])
        dec_part = " ".join(nums[int(d)] for d in parts[1])

        text = text.replace(key, f"{int_part} phẩy {dec_part}")

    return text
