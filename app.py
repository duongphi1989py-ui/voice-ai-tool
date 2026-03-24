import streamlit as st
import asyncio
import edge_tts
import re
import random

st.set_page_config(page_title="Voice Story AI Pro", page_icon="🎬")

st.title("🎬 Voice Story AI Pro Max")
st.write("Text → Voice kể chuyện + ngắt nghỉ tự động")

# ================= INPUT =================
text = st.text_area("Nhập nội dung:", height=250)

# ================= VOICES =================
voices = {
    "Nữ Việt Nam": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural",
    "Nữ US": "en-US-JennyNeural",
    "Nam US": "en-US-GuyNeural"
}

voice_name = st.selectbox("Chọn giọng:", list(voices.keys()))

# ================= RATE (FIX CHUẨN EDGE-TTS) =================
rate_map = {
    "Chậm": "-10%",
    "Bình thường": "+0%",
    "Nhanh": "+10%"
}

rate_name = st.selectbox("Tốc độ:", list(rate_map.keys()))

# ================= STORY MODE =================
story_mode = st.toggle("🎭 Story Mode (ngắt nghỉ tự nhiên)", value=True)

# ================= AUTO PAUSE ENGINE =================
def story_engine(text):
    text = text.strip()

    # xuống dòng = nghỉ
    text = text.replace("\n", " ... ")

    # dấu câu = pause
    text = re.sub(r"\.", ". ... ", text)
    text = re.sub(r",", ", ... ", text)
    text = re.sub(r"!", "! ... ", text)
    text = re.sub(r"\?", "? ... ", text)

    # tăng cảm giác kể chuyện
    text = text.replace("...", " ...... ")

    # random pause nhẹ (giống người thật)
    if story_mode:
        words = text.split()
        new_text = []
        for w in words:
            new_text.append(w)
            if random.random() < 0.03:
                new_text.append(" ... ")
        return " ".join(new_text)

    return text

# ================= GENERATE VOICE =================
async def generate_voice(text, voice, rate):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate
    )
    await communicate.save("voice.mp3")

# ================= RUN =================
if st.button("🚀 Tạo giọng nói"):

    if not text:
        st.warning("⚠️ Nhập nội dung trước!")
    else:

        final_text = story_engine(text)

        with st.spinner("🎧 Đang tạo giọng AI..."):
            asyncio.run(
                generate_voice(
                    final_text,
                    voices[voice_name],
                    rate_map[rate_name]
                )
            )

        st.success("✅ Xong!")

        st.audio("voice.mp3")

        with open("voice.mp3", "rb") as f:
            st.download_button("📥 Tải MP3", f, file_name="story.mp3")
        st.audio("voice.mp3")

        with open("voice.mp3", "rb") as f:
            st.download_button("📥 Tải MP3", f, file_name="story.mp3")
