import streamlit as st
import asyncio
import edge_tts
import re
import random
import uuid

st.set_page_config(page_title="Voice AI SaaS Pro", page_icon="🎙️")

st.title("🎙️ Voice AI SaaS PRO (Smooth Version)")
st.write("Text → Voice AI mượt như người thật")

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
    "Tự nhiên": {"rate": "+0%", "pitch": "+0Hz"},
    "Vui vẻ": {"rate": "+15%", "pitch": "+20Hz"},
    "Buồn": {"rate": "-15%", "pitch": "-20Hz"},
    "Kể chuyện": {"rate": "-5%", "pitch": "+0Hz"},
    "Quảng cáo": {"rate": "+20%", "pitch": "+10Hz"}
}
emotion_name = st.selectbox("🎭 Emotion", list(emotion_map.keys()))

# ================= PAUSE =================
st.subheader("⏱️ Ngắt nghỉ")

pause_dot = st.slider("Dấu chấm (.)", 0.0, 0.8, 0.3, 0.1)
pause_comma = st.slider("Dấu phẩy (,)", 0.0, 0.5, 0.2, 0.1)
pause_exclaim = st.slider("Dấu !", 0.0, 0.8, 0.4, 0.1)

# ================= TEXT ENGINE (SSML) =================
def story_engine(text, cfg):
    text = text.strip()

    # xuống dòng
    text = text.replace("\n", '<break time="500ms"/>')

    # dấu câu
    text = re.sub(r"\.", f'.<break time="{int(cfg["dot"]*1000)}ms"/>', text)
    text = re.sub(r",", f',<break time="{int(cfg["comma"]*1000)}ms"/>', text)
    text = re.sub(r"!", f'!<break time="{int(cfg["exclaim"]*1000)}ms"/>', text)

    return text

cfg = {
    "dot": pause_dot,
    "comma": pause_comma,
    "exclaim": pause_exclaim
}

# ================= SPLIT TEXT =================
def split_text(text, max_length=400):
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
async def generate_long_voice(text, voice, rate, pitch, file_name):
    chunks = split_text(text)

    open(file_name, "wb").close()

    for i, chunk in enumerate(chunks):

        ssml = f"""
        <speak>
            <prosody rate="{rate}" pitch="{pitch}">
                {chunk}
            </prosody>
        </speak>
        """

        temp_file = f"temp_{i}.mp3"

        communicate = edge_tts.Communicate(
            text=ssml,
            voice=voice
        )
        await communicate.save(temp_file)

        # nối file mượt hơn
        with open(file_name, "ab") as final:
            with open(temp_file, "rb") as f:
                final.write(f.read())

        await asyncio.sleep(0.05)  # chống click

# ================= CACHE =================
@st.cache_data
def cached_generate(text, voice, rate, pitch):
    file_name = f"cache_{hash(text + voice + rate + pitch)}.mp3"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        generate_long_voice(text, voice, rate, pitch, file_name)
    )

    return file_name

# ================= RUN =================
if st.button("🚀 Generate Voice"):

    if not text:
        st.warning("Nhập nội dung trước!")
    else:
        emotion = emotion_map[emotion_name]

        final_text = story_engine(text, cfg)

        with st.spinner("🎧 Đang tạo voice..."):
            file_name = cached_generate(
                final_text,
                voices[voice_name],
                emotion["rate"],
                emotion["pitch"]
            )

        st.success("✅ Done!")

        st.audio(file_name)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Tải MP3",
                f,
                file_name="voice.mp3"
            )
