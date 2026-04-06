import streamlit as st
import asyncio
import edge_tts
import re
import os
import hashlib

# ===== IMPORT TEXT PROCESS =====
from tts_utils.text_processor import final_process

# ================= CONFIG =================
st.set_page_config(page_title="Voice AI PRO", page_icon="🎙️")
st.title("🎙️ Voice AI PRO MAX (Smooth Vietnamese Voice)")
st.write("Giọng đọc tự nhiên – không vấp – có nhịp như người")

# ================= SESSION =================
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# ================= UTILS =================
def get_hash(text, voice, rate):
    raw = text + voice + rate
    return hashlib.md5(raw.encode()).hexdigest()

# ================= GENERATE =================
async def generate_voice(text, voice, rate, file_name):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate
    )
    await communicate.save(file_name)

# ================= CACHE =================
@st.cache_data
def cached_generate(text, voice, rate):
    file_name = f"cache_{get_hash(text, voice, rate)}.mp3"

    if not os.path.exists(file_name):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            generate_voice(text, voice, rate, file_name)
        )

    return file_name

# ================= UI =================
text = st.text_area("Nhập nội dung:", height=300, key="text_input")

def clear_text():
    st.session_state["text_input"] = ""

st.button("🗑️ Xóa nhanh", on_click=clear_text)

voices = {
    "Nữ Việt Nam (mượt nhất)": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural"
}
voice_name = st.selectbox("Chọn giọng:", list(voices.keys()))

rate_map = {
    "Chậm": "-10%",
    "Bình thường": "+0%",
    "Nhanh": "+10%"
}
rate_name = st.selectbox("Tốc độ:", list(rate_map.keys()))

# ================= MAIN =================
if st.button("🚀 Generate Voice"):

    if not text:
        st.warning("Nhập nội dung trước!")
    else:
        # ===== FLOW CHUẨN =====
        final_text = final_process(text)
        # debug nếu cần
        # st.write(final_text)

        with st.spinner("🎧 Đang tạo voice..."):
            file_name = cached_generate(
                final_text,
                voices[voice_name],
                rate_map[rate_name]
            )

        st.success("✅ Done!")
        st.audio(file_name)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Tải MP3",
                f,
                file_name="voice.mp3"
            )

# ================= CLEAR CACHE =================
if st.button("🧹 Clear cache"):
    st.cache_data.clear()
    st.success("Đã xóa cache!")
