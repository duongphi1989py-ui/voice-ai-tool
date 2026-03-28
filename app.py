import streamlit as st
import asyncio
import edge_tts
import re
import random
import uuid

st.set_page_config(page_title="Voice AI SaaS Pro", page_icon="🎙️")

st.title("🎙️ Voice AI SaaS PRO (Smooth Real Voice)")
st.write("Không dùng SSML → không đọc 'break time'")

# ================= TEXT =================
text = st.text_area("Nhập nội dung:", height=250)

# ================= VOICES =================
voices = {
    "Nữ Việt Nam": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural",
    "Nữ US": "en-US-JennyNeural",
    "Nam US": "en-US-GuyNeural"
}
voice_name = st.selectbox("Chọn giọng:", list(voices.keys()))

# ================= EMOTION =================
emotion_map = {
    "Tự nhiên": "+0%",
    "Vui vẻ": "+15%",
    "Buồn": "-15%",
    "Kể chuyện": "-5%",
    "Quảng cáo": "+20%"
}
emotion_name = st.selectbox("🎭 Emotion", list(emotion_map.keys()))

# ================= STORY ENGINE =================
def story_engine(text):
    text = text.strip()

    # xuống dòng → nghỉ nhẹ
    text = text.replace("\n", ". ")

    # tăng nhịp tự nhiên
    text = re.sub(r"\.", ". ", text)
    text = re.sub(r",", ", ", text)
    text = re.sub(r"!", "! ", text)

    # random pause nhẹ (giống người)
    words = text.split()
    out = []

    for w in words:
        out.append(w)
        if random.random() < 0.03:
            out.append("...")

    return " ".join(out)

# ================= SPLIT =================
def split_text(text, max_length=250):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""

    for s in sentences:
        if len(current) + len(s) < max_length:
            current += " " + s
        else:
            chunks.append(current.strip())
            current = s

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

        await asyncio.sleep(0.1)  # chống click

# ================= CACHE =================
@st.cache_data
def cached_generate(text, voice, rate):
    file_name = f"cache_{hash(text + voice + rate)}.mp3"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        generate_voice(text, voice, rate, file_name)
    )

    return file_name

# ================= RUN =================
if st.button("🚀 Generate Voice"):

    if not text:
        st.warning("Nhập nội dung trước!")
    else:
        final_text = story_engine(text)

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
