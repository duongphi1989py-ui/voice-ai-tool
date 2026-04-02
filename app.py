import streamlit as st
import asyncio
import edge_tts
import re
import random
import os
import hashlib

from tts_utils.text_processor import (
    process_text,
    fix_upper_after_dot,
    fix_numbers_ultimate,
    story_engine
)

# ================= CONFIG =================
st.set_page_config(page_title="Voice AI SaaS Pro", page_icon="🎙️")

st.title("🎙️ Voice AI SaaS PRO (Smooth Real Voice)")
st.write("Không dùng SSML → đọc mượt như người")

# ================= SESSION STATE =================
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# ================= UTILS =================
# ================= UI PRO =================

st.markdown("## 🎙️ Voice AI Studio")

col_left, col_right = st.columns([3, 1])  # 👈 trái to, phải nhỏ

# ===== CỘT TRÁI (TEXT) =====
with col_left:
    st.markdown("### 📝 Nội dung")

    text = st.text_area(
        "",
        height=500,   # 👈 to dễ nhìn
        key="text_input",
        placeholder="Nhập nội dung dài ở đây..."
    )

    # nút xoá
    def clear_text():
        

    st.button("🗑️ Xóa nội dung", on_click=clear_text)

# ===== CỘT PHẢI (CONTROL + AUDIO) =====
with col_right:
    st.markdown("### ⚙️ Cài đặt")

    voices = {
        "Nữ VN": "vi-VN-HoaiMyNeural",
        "Nam VN": "vi-VN-NamMinhNeural",
        "Nữ US": "en-US-JennyNeural",
        "Nam US": "en-US-GuyNeural"
    }
    voice_name = st.selectbox("Giọng đọc", list(voices.keys()))

    emotion_map = {
        "Tự nhiên": "+0%",
        "Vui": "+15%",
        "Buồn": "-15%",
        "Kể chuyện": "-5%",
        "QC": "+20%"
    }
    emotion_name = st.selectbox("Emotion", list(emotion_map.keys()))

    st.markdown("---")

    generate_btn = st.button("🚀 Generate", use_container_width=True)

    st.markdown("---")

    audio_placeholder = st.empty()

# ================= RUN =================
if generate_btn:

    if not text:
        st.warning("Nhập nội dung trước!")
    else:
        processed_text = process_text(text)
        processed_text = fix_numbers_ultimate(processed_text)
        processed_text = fix_upper_after_dot(processed_text)

        final_text = story_engine(processed_text)

        with st.spinner("🎧 Đang tạo voice..."):
            file_name = cached_generate(
                final_text,
                voices[voice_name],
                emotion_map[emotion_name]
            )

        st.success("✅ Done!")

        # 👉 audio nằm bên phải
        with col_right:
            audio_placeholder.audio(file_name)

            with open(file_name, "rb") as f:
                st.download_button(
                    "📥 Tải MP3",
                    f,
                    file_name="voice.mp3",
                    use_container_width=True
                )

# ================= GENERATE =================
async def generate_voice(text, voice, rate, file_name):
    chunks = split_text(text)

    open(file_name, "wb").close()

    for i, chunk in enumerate(chunks):
        temp_file = f"temp_{i}.mp3"

        communicate = edge_tts.Communicate(
            text=chunk,
            voice=voice,
            rate=rate
        )
        await communicate.save(temp_file)

        with open(file_name, "ab") as final:
            with open(temp_file, "rb") as f:
                final.write(f.read())

        await asyncio.sleep(0.12)  # 🔥 mượt hơn

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
text = st.text_area(
    "Nhập nội dung:",
    height=250,
    key="text_input"
)

def clear_text():
    st.session_state["text_input"] = ""

st.button("🗑️ Xóa nhanh", on_click=clear_text)

voices = {
    "Nữ Việt Nam": "vi-VN-HoaiMyNeural",
    "Nam Việt Nam": "vi-VN-NamMinhNeural",
    "Nữ US": "en-US-JennyNeural",
    "Nam US": "en-US-GuyNeural"
}
voice_name = st.selectbox("Chọn giọng:", list(voices.keys()))

emotion_map = {
    "Tự nhiên": "+0%",
    "Vui vẻ": "+15%",
    "Buồn": "-15%",
    "Kể chuyện": "-5%",
    "Quảng cáo": "+20%"
}
emotion_name = st.selectbox("🎭 Emotion", list(emotion_map.keys()))

# ================= RUN =================
if st.button("🚀 Generate Voice"):

    if not text:
        st.warning("Nhập nội dung trước!")
    else:
        # 🔥 FLOW FINAL
        processed_text = process_text(text)

        processed_text = fix_numbers_ultimate(processed_text)

        processed_text = fix_upper_after_dot(processed_text)

       
        # 🔥 giảm pause dấu chấm
       

        # clean space
        processed_text = re.sub(r'\s+', ' ', processed_text)
        processed_text = processed_text.replace("  ", " ")

        final_text = story_engine(processed_text)

        # DEBUG nếu cần
        # st.write(final_text)

        with st.spinner("🎧 Đang tạo voice..."):
            file_name = cached_generate(
                final_text,
                voices[voice_name],
                emotion_map[emotion_name]
            )

        st.success("✅ Done!")
        st.audio(file_name)

        with open(file_name, "rb") as f:
            st.download_button(
                "📥 Tải MP3",
                f,
                file_name="voice.mp3"
            )
