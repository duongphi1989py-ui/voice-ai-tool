import streamlit as st
import asyncio
import edge_tts

st.set_page_config(page_title="Voice AI Pro Max", page_icon="🎤")

st.title("🎤 Voice AI Pro Max (Stable Version)")
st.write("Text → Voice AI (giọng tự nhiên, ổn định)")

# ===== TEXT INPUT =====
text = st.text_area("Nhập văn bản:", height=200)

# ===== VOICE LIST =====
voices = {
    "Nữ Việt Nam (Hoài My)": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam (Minh)": "vi-VN-NamMinhNeural",
    "Nữ US (Jenny)": "en-US-JennyNeural",
    "Nam US (Guy)": "en-US-GuyNeural"
}

voice = st.selectbox("Chọn giọng:", list(voices.keys()))

# ===== SPEED =====
rate = st.selectbox(
    "Tốc độ đọc:",
    ["-20%", "-10%", "0%", "+10%", "+20%"]
)

# ===== ASYNC FUNCTION =====
async def make_voice(text, voice_id, rate):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice_id,
        rate=rate
    )
    await communicate.save("voice.mp3")

# ===== BUTTON =====
if st.button("🚀 Tạo giọng nói"):

    if not text:
        st.warning("⚠️ Vui lòng nhập nội dung!")
    else:
        with st.spinner("🎧 Đang tạo giọng AI..."):

            asyncio.run(
                make_voice(text, voices[voice], rate)
            )

        st.success("✅ Hoàn thành!")

        # PLAY AUDIO
        st.audio("voice.mp3")

        # DOWNLOAD BUTTON
        with open("voice.mp3", "rb") as f:
            st.download_button(
                "📥 Tải file MP3",
                f,
                file_name="voice.mp3"
            )
