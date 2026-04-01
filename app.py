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

# ================= STORY ENGINE =================
def story_engine(text):
    text = text.strip()

    # xuống dòng → nghỉ nhẹ
    text = text.replace("\n", ". ")

    # nhịp nhẹ
    text = re.sub(r",", ", ", text)
    text = re.sub(r"!", "! ", text)

    return text

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
    chunks = split_text(text)

    open(file_name, "wb").close()

    for i, chunk in enumerate(chunks):
        temp_file = f"temp_{i}.mp3"

        communicate = edge_tts.Communicate(
            text=chunk,
            voice=voice,
            rate=rate
        )
        await communicate.save(temp_file)

        with open(file_name, "ab") as final:
            with open(temp_file, "rb") as f:
                final.write(f.read())

        await asyncio.sleep(0.05)

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
        # 🔥 PROCESS FLOW CHUẨN
        processed_text = process_text(text)
        processed_text = fix_upper_after_dot(processed_text)
        processed_text = processed_text.replace(". ", ", ")
        final_text = story_engine(processed_text)

        # Debug nếu cần
        # st.write(final_text)

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
