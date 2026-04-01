import streamlit as st
import asyncio
import edge_tts
import re
import random
import os
import hashlib

from tts_utils.text_processor import process_text, fix_upper_after_dot

# ================= CONFIG =================
st.set_page_config(page_title="Voice AI SaaS Pro", page_icon="🎙️")

st.title("🎙️ Voice AI SaaS PRO (Smooth Real Voice)")
st.write("Không dùng SSML → không đọc 'break time'")

# ================= UTILS =================
def get_hash(text, voice, rate):
    raw = text + voice + rate
    return hashlib.md5(raw.encode()).hexdigest()

# 🔥 FIX QUOTES
def fix_quotes(text: str) -> str:
    return re.sub(r'"(.*?)"', r', \1,', text)

# ================= STORY ENGINE =================
def story_engine(text):
    text = text.strip()

    text = text.replace("\n", ", ")
    text = re.sub(r",", ", ", text)
    text = re.sub(r"!", "! ", text)

    return text

# ================= PRESET =================
def apply_preset(text, rate, preset_name):
    if preset_name == "🎧 Truyện":
        text = text.replace(". ", ", ")
        text = text.replace("!", ", ")
        text = text.replace("?", ", ")
        rate = "-5%"

    elif preset_name == "🎬 TikTok":
        text = text.replace(". ", ", ")
        rate = "+12%"

    elif preset_name == "📢 Quảng cáo":
        text = text.replace(". ", "! ")
        rate = "+18%"

    return text, rate

# ================= SPLIT =================
def split_text(text, max_length=1200):
    sentences = text.split(". ")
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_length:
            current += sentence + ". "
        else:
            chunks.append(current.strip())
            current = sentence + ". "

    if current:
        chunks.append(current.strip())

    return chunks

# ================= GENERATE =================
async def generate_voice(text, voice, rate, file_name):

    chunks = split_text(text, max_length=1200)

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

                # 🔥 bỏ header MP3 từ chunk sau → tránh khựng
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
            generate_voice_stream(text, voice, rate, file_name)
        )

    return file_name

# ================= UI =================
text = st.text_area("Nhập nội dung:", height=250)

voices = {
    "Nữ Việt Nam": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural",
    "Nữ US": "en-US-JennyNeural",
    "Nam US": "en-US-GuyNeural"
}
voice_name = st.selectbox("Chọn giọng:", list(voices.keys()))

emotion_map = {
    "Tự nhiên": "+0%",
    "Vui vẻ": "+10%",
    "Buồn": "-10%",
    "Kể chuyện": "-5%",
    "Quảng cáo": "+15%"
}
emotion_name = st.selectbox("🎭 Emotion", list(emotion_map.keys()))

# 🔥 PRESET UI
preset = st.selectbox(
    "🎚️ Preset giọng",
    ["Giữ nguyên", "🎧 Truyện", "🎬 TikTok", "📢 Quảng cáo"]
)

# ================= RUN =================
if st.button("🚀 Generate Voice"):

    if not text:
        st.warning("Nhập nội dung trước!")
    else:
        # 🔥 PROCESS
        processed_text = process_text(text)
        processed_text = fix_upper_after_dot(processed_text)
        processed_text = fix_quotes(processed_text)

        final_text = story_engine(processed_text)

        # 🔥 APPLY PRESET (không phá config cũ)
        final_text, final_rate = apply_preset(
            final_text,
            emotion_map[emotion_name],
            preset
        )

        with st.spinner("🎧 Đang tạo voice..."):
            file_name = cached_generate(
                final_text,
                voices[voice_name],
                final_rate
            )

        st.success("✅ Done!")
        st.audio(file_name)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Tải MP3",
                f,
                file_name="voice.mp3"
            )
