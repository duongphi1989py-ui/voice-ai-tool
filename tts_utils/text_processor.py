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
def fix_numbers_level_max(text: str) -> str:

    # giờ
    text = re.sub(r'\b(\d{1,2})[:h](\d{1,2})\b', read_time, text)

    # %
    text = re.sub(r'\b(\d+)%', read_percent, text)

    # tiền VND
    text = re.sub(r'\b(\d+)[\.,]?\d*đ', read_money, text)

    # k, tr
    text = re.sub(r'\b(\d+)(k|tr)\b', read_short_money, text)

    # đơn vị
    text = re.sub(r'\b(\d+)(km|kg|m)\b', read_unit, text)

    # số dạng 1,000
    text = re.sub(r'\b\d{1,3}(,\d{3})+\b',
                  lambda m: read_number(m.group().replace(",", "")), text)

    # số thập phân
    text = re.sub(r'\b(\d+)\.(\d+)\b', read_decimal, text)

    # số thường
    text = re.sub(r'\b\d+\b', lambda m: read_number(m.group()), text)

    return text
