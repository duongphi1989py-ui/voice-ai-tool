import streamlit as st
import asyncio
import edge_tts
import os

st.set_page_config(page_title="Voice AI Pro Max", page_icon="🎤")

st.title("🎤 Voice AI Pro Max (Giọng xịn hơn)")

text = st.text_area("Nhập văn bản:", height=200)

voices = {
    "Nữ Việt Nam": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural",
    "Nữ US": "en-US-JennyNeural",
    "Nam US": "en-US-GuyNeural"
}


rate = st.selectbox(
    "Tốc độ:",
    ["-10%", "0%", "+10%"]
)

# async function
async def make_voice(text, voice, rate):
    communicate = edge_tts.Communicate(
    text=text,
    voice=voices[voice],
    rate=rate
)
    await communicate.save("voice.mp3")

if st.button("🚀 Tạo giọng nói"):

    if not text:
        st.warning("Nhập nội dung trước!")
    else:
        with st.spinner("Đang tạo giọng AI..."):

            asyncio.run(make_voice(text, voice, rate))

        st.success("✅ Xong!")

        st.audio("voice.mp3")

        with open("voice.mp3", "rb") as f:
            st.download_button("📥 Tải file MP3", f, file_name="voice.mp3")
