import streamlit as st
import asyncio
import edge_tts
import re
import random
import os
import hashlib
from tts_utils.text_processor import process_text, fix_upper_after_dot, fix_numbers_level_max
# ================= CONFIG =================
st.set_page_config(page_title="Voice AI SaaS Pro", page_icon="🎙️")

st.title("🎙️ Voice AI SaaS PRO (Smooth Real Voice)")
st.write("Không khựng giữa câu – nghỉ tự nhiên như người")

# ================= UTILS =================
def get_hash(text, voice, rate):
    raw = text + voice + rate
    return hashlib.md5(raw.encode()).hexdigest()

# ================= TEXT PROCESS =================
def process_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)

    text = text.replace('"', ', ')
    text = text.replace(",", ", ")
    text = text.replace(".", ". ")
    text = text.replace("!", "! ")
    text = text.replace("?", "? ")

    return text.strip()

def fix_upper_after_dot(text):
    def lower_match(m):
        return m.group(0).lower()

    return re.sub(
        r'(?<=[.!?])\s+[“"\'(]*[A-ZĐ]',
        lower_match,
        text
    )
def soften_dots(text):
    sentences = text.split(". ")
    result = []

    for i, s in enumerate(sentences):
        if i < len(sentences) - 1:
            if random.random() < 0.7:
                result.append(s + ", ")
            else:
                result.append(s + ". ")
        else:
            result.append(s)

    return "".join(result)
# ================= STORY ENGINE =================
def story_engine(text):
    text = text.strip()

    text = text.replace("\n", ". ")

    return text

# ================= SPLIT CHUẨN =================
def split_text(text, max_length=1300):
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) <= max_length:
            current += sentence + " "
        else:
            chunks.append(current.strip())
            current = sentence + " "

    if current:
        chunks.append(current.strip())

    return chunks

# ================= GENERATE =================
async def generate_voice(text, voice, rate, file_name):

    chunks = split_text(text)

    with open(file_name, "wb") as final:

        for i, chunk in enumerate(chunks):

            communicate = edge_tts.Communicate(
                text=chunk,
                voice=voice,
                rate=rate
            )

            temp_file = f"temp_{i}.mp3"
            await communicate.save(temp_file)

            with open(temp_file, "rb") as f:
                data = f.read()

                # 🔥 bỏ header tránh khựng
                if i > 0:
                    data = data[300:]

                final.write(data)

            await asyncio.sleep(0.02)

# ================= CACHE =================
@st.cache_data
def cached_generate(text, voice, rate):
    file_name = f"cache_{get_hash(text, voice, rate)}.mp3"

    if not os.path.exists(file_name):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            generate_voice(text, voice, rate, file_name)
        )

    return file_name

# ================= UI =================
def clear_text():
    st.session_state.text_input = ""

if "text_input" not in st.session_state:
    st.session_state.text_input = ""

text = st.text_area("Nhập nội dung:", height=250, key="text_input")

st.button("🗑️ Xoá nhanh", on_click=clear_text)



voices = {
    "Nữ Việt Nam": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural",
    "Nữ US": "en-US-JennyNeural",
    "Nam US": "en-US-GuyNeural"
}
voice_name = st.selectbox("Chọn giọng:", list(voices.keys()))

emotion_map = {
    "Tự nhiên": "+0%",
    "Vui vẻ": "+15%",
    "Buồn": "-15%",
    "Kể chuyện": "-5%",
    "Quảng cáo": "+20%"
}
emotion_name = st.selectbox("🎭 Emotion", list(emotion_map.keys()))

# ================= RUN =================
if st.button("🚀 Generate Voice"):

    if not text:
        st.warning("Nhập nội dung trước!")
    else:
        # 🔥 FLOW FINAL FIX 100%

# 1. protect decimal trước khi bị phá
        processed_text, decimals = protect_decimal(text)

# 2. xử lý bình thường
        processed_text = process_text(processed_text)

        processed_text = fix_upper_after_dot(processed_text)

        processed_text = fix_numbers_level_max(processed_text)

        processed_text = soften_dots(processed_text)

        processed_text = re.sub(r'\s+', ' ', processed_text)

# 3. restore decimal (QUAN TRỌNG)
        processed_text = restore_decimal(processed_text, decimals)

        final_text = story_engine(processed_text)
        with st.spinner("🎧 Đang tạo voice..."):
            file_name = cached_generate(
                final_text,
                voices[voice_name],
                emotion_map[emotion_name]
            )

        st.success("✅ Done!")
        st.audio(file_name)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Tải MP3",
                f,
                file_name="voice.mp3"
            )
