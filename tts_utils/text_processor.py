import re

def process_text(text: str) -> str:
    """
    Xử lý văn bản để thêm pause theo dấu câu
    """

    # Chuẩn hóa xuống dòng
    text = re.sub(r'\n+', '\n', text)

    # Thêm pause theo dấu
    text = text.replace(",", ", <break time='200ms'/>")
    text = text.replace(".", ". <break time='100ms'/>")
    text = text.replace(":", ": <break time='100ms'/>")

    # Xuống dòng -> nghỉ lâu hơn
    text = text.replace("\n", "\n<break time='300ms'/>")

    return text
