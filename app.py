import streamlit as st
import asyncio
import edge_tts
import re
import random
import uuid

st.set_page_config(page_title="Voice AI SaaS Pro", page_icon="🎙️")

st.title("🎙️ Voice AI SaaS PRO (Stable + Story Engine)")
st.write("Text → Voice AI + chỉnh ngắt nghỉ siêu mượt")

# ================= TEXT =================
text = st.text_area("Nhập nội dung:", height=250)

# ================= VOICES =================
voices = {
    "Nữ Việt Nam": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural",
    "Nữ US": "en-US-JennyNeural",
    "Nam US": "en-US-GuyNeural"
}

voice_name = st.selectbox("Chọn giọng:", list(voices.keys()), key="voice_select")

# ================= RATE =================
rate_map = {
    "Chậm": "-10%",
    "Bình thường": "+0%",
    "Nhanh": "+10%"
}

rate_name = st.selectbox("Tốc độ:", list(rate_map.keys()), key="rate_select")

# ================= STORY MODE =================
story_mode = st.toggle("🎭 Story Mode (tự nhiên hơn)", value=True, key="story_mode")

# ================= PAUSE CONTROL (0.1 → 0.5) =================
st.subheader("⏱️ Ngắt nghỉ tùy chỉnh")

pause_dot = st.slider("Dấu chấm (.)", 0.0, 0.5, 0.2, 0.1)
pause_comma = st.slider("Dấu phẩy (,)", 0.0, 0.5, 0.1, 0.1)
pause_exclaim = st.slider("Dấu !", 0.0, 0.5, 0.3, 0.1)
pause_newline = st.slider("Xuống dòng", 0.0, 0.5, 0.4, 0.1)

# ================= TEXT ENGINE =================
def story_engine(text, cfg):
    text = text.strip()

    text = text.replace("\n", " ... ")

    text = re.sub(r"\.", ". ... " * int(cfg["dot"] * 5 + 1), text)
    text = re.sub(r",", ", ... " * int(cfg["comma"] * 5 + 1), text)
    text = re.sub(r"!", "! ... " * int(cfg["exclaim"] * 5 + 1), text)

    if story_mode:
        words = text.split()
        out = []
        for w in words:
            out.append(w)
            if random.random() < 0.02:
                out.append(" ... ")
        return " ".join(out)

    return text

# ================= CONFIG =================
cfg = {
    "dot": pause_dot,
    "comma": pause_comma,
    "exclaim": pause_exclaim,
    "newline": pause_newline
}

# ================= AUDIO =================
async def generate_voice(text, voice, rate):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate
    )
    await communicate.save("voice.mp3")

# ================= RUN =================
if st.button("🚀 Generate Voice", key="generate_btn"):

    if not text:
        st.warning("Nhập nội dung trước!")
    else:

        final_text = story_engine(text, cfg)

        with st.spinner("🎧 Đang tạo voice..."):
            asyncio.run(
                generate_voice(
                    final_text,
                    voices[voice_name],
                    rate_map[rate_name]
                )
            )

        st.success("✅ Done!")

    st.audio("voice.mp3")
        with open("voice.mp3", "rb") as f:
            st.download_button(
                "📥 Download MP3",
                f,
                file_name="voice.mp3",
                key=f"download_{uuid.uuid4()}"
            )
        st.audio("voice.mp3")

        with open("voice.mp3", "rb") as f:
            st.download_button("📥 Tải MP3", f, file_name="story.mp3")
