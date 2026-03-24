import streamlit as st
import asyncio
import edge_tts
from utils import auto_pause

st.set_page_config(page_title="Voice AI Pro", page_icon="🎤")

st.title("🎤 Voice AI Pro System")

text = st.text_area("Nhập văn bản:", height=200)

voices = {
    "Nữ Việt Nam": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural",
    "Nữ US": "en-US-JennyNeural",
    "Nam US": "en-US-GuyNeural"
}

voice = st.selectbox("Chọn giọng:", list(voices.keys()))

rate_map = {
    "Chậm": "-10%",
    "Bình thường": "+0%",
    "Nhanh": "+10%"
}

rate = st.selectbox("Tốc độ:", list(rate_map.keys()))

auto_break = st.toggle("🎙️ Ngắt nghỉ tự động (Pro mode)", value=True)

async def generate(text, voice_id, rate):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice_id,
        rate=rate
    )
    await communicate.save("voice.mp3")

if st.button("🚀 Tạo giọng nói"):

    if not text:
        st.warning("Nhập nội dung!")
    else:

        final_text = auto_pause(text) if auto_break else text

        with st.spinner("Đang xử lý AI..."):
            asyncio.run(
                generate(final_text, voices[voice], rate_map[rate])
            )

        st.success("Done!")

        st.audio("voice.mp3")

        with open("voice.mp3", "rb") as f:
            st.download_button("Download MP3", f, file_name="voice.mp3")
