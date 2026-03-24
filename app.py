import streamlit as st
from gtts import gTTS
import os

st.set_page_config(page_title="Voice AI Stable", page_icon="🎤")

st.title("🎤 Voice AI Stable Tool")
st.write("Text → Voice (chạy ổn định 100%)")

text = st.text_area("Nhập văn bản:", height=200)

lang = st.selectbox(
    "Chọn ngôn ngữ:",
    ["Tiếng Việt", "English"]
)

lang_map = {
    "Tiếng Việt": "vi",
    "English": "en"
}

if st.button("🚀 Tạo giọng nói"):

    if not text:
        st.warning("Vui lòng nhập nội dung!")
    else:
        tts = gTTS(text=text, lang=lang_map[lang])

        file_path = "voice.mp3"
        tts.save(file_path)

        st.success("✅ Tạo thành công!")

        st.audio(file_path)

        with open(file_path, "rb") as f:
            st.download_button("📥 Tải file MP3", f, file_name="voice.mp3")
