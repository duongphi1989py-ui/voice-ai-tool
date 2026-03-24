import streamlit as st
import asyncio
import edge_tts
import re
import random

st.set_page_config(page_title="Voice Storytelling Pro Max", page_icon="🎬")

st.title("🎬 Voice Storytelling PRO MAX")
st.write("Text → Voice kể chuyện kiểu TikTok / YouTube")

# ================= TEXT =================
text = st.text_area("Nhập nội dung truyện:", height=250)

# ================= VOICES =================
voices = {
    "Nữ Việt Nam": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural",
    "Nữ US (Story)": "en-US-JennyNeural",
    "Nam US (Deep)": "en-US-GuyNeural"
}

voice_name = st.selectbox("Chọn giọng:", list(voices.keys()))

# ================= STORY MODE =================
story_mode = st.toggle("🎭 Story Mode (tự nhiên như người kể chuyện)", value=True)

# ================= SPEED =================
rate = st.selectbox("Tốc độ:", ["-10%", "0%", "+10%"])

# ================= PRO PAUSE ENGINE =================
def story_pause_engine(text):
    # làm sạch cơ bản
    text = text.strip()

    # xuống dòng = pause dài
    text = text.replace("\n", " ... ")

    # dấu câu = ngắt nghỉ
    text = re.sub(r"\.", ". ... ", text)
    text = re.sub(r",", ", ... ", text)
    text = re.sub(r"!", "! ... ", text)
    text = re.sub(r"\?", "? ... ", text)

    # tăng cảm giác kể chuyện
    text = text.replace("...", " ...... ")

    # thêm random nhẹ để giống người thật
    words = text.split(" ")
    result = []

    for w in words:
        result.append(w)

        if story_mode:
            # random pause nhỏ để tự nhiên hơn
            if random.random() < 0.03:
                result.append(" ... ")

    return " ".join(result)

# ================= AUDIO ENGINE =================
async def generate_voice(text, voice, rate):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate
    )
    await communicate.save("voice.mp3")

# ================= RUN =================
if st.button("🚀 Generate Story Voice"):

    if not text:
        st.warning("Nhập nội dung trước đã!")
    else:

        final_text = story_pause_engine(text) if story_mode else text

        with st.spinner("🎧 Đang tạo giọng kể chuyện..."):
            asyncio.run(
                generate_voice(final_text, voices[voice_name], rate)
            )

        st.success("✅ Done!")

        st.audio("voice.mp3")

        with open("voice.mp3", "rb") as f:
            st.download_button("📥 Tải MP3", f, file_name="story.mp3")
