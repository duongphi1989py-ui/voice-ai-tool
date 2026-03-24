import streamlit as st
import asyncio
import edge_tts

st.set_page_config(page_title="Voice AI Stable", page_icon="🎤")

st.title("🎤 Voice AI Stable (No Error Version)")
st.write("Text → Voice AI ổn định cho Streamlit Cloud")

# ===== INPUT TEXT =====
text = st.text_area("Nhập văn bản:", height=200)

# ===== VOICES =====
voices = {
    "Nữ Việt Nam": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural",
    "Nữ US": "en-US-JennyNeural",
    "Nam US": "en-US-GuyNeural"
}

voice_name = st.selectbox("Chọn giọng:", list(voices.keys()))

# ===== RATE (FIX CHUẨN EDGE-TTS) =====
rate_options = {
    "Rất chậm": "-20%",
    "Chậm": "-10%",
    "Bình thường": "+0%",
    "Nhanh": "+10%",
    "Rất nhanh": "+20%"
}

rate_name = st.selectbox("Tốc độ:", list(rate_options.keys()))

# ===== ASYNC FUNCTION =====
async def generate_voice(text, voice, rate):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate
    )
    await communicate.save("voice.mp3")

# ===== BUTTON =====
if st.button("🚀 Tạo giọng nói"):

    if not text:
        st.warning("⚠️ Bạn chưa nhập nội dung!")
    else:
        with st.spinner("🎧 Đang tạo giọng AI..."):

            asyncio.run(
                generate_voice(
                    text,
                    voices[voice_name],
                    rate_options[rate_name]
                )
            )

        st.success("✅ Hoàn thành!")

        # PLAY AUDIO
        st.audio("voice.mp3")

        # DOWNLOAD
        with open("voice.mp3", "rb") as f:
            st.download_button(
                "📥 Tải file MP3",
                f,
                file_name="voice.mp3"
            )
