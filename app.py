import streamlit as st
from elevenlabs.client import ElevenLabs

st.set_page_config(page_title="Voice AI Pro", page_icon="🎤")

st.title("🎤 Voice AI Pro")

api_key = st.secrets["ELEVEN_API_KEY"]
text = st.text_area("Nhập văn bản:", height=200)

voice_id = st.selectbox("Chọn giọng:", ["Rachel", "Adam"])

voice_map = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Adam": "pNInz6obpgDQGcFmaJgB"
}

if st.button("🚀 Tạo giọng nói"):

    if not api_key:
        st.warning("Thiếu API key!")
    elif not text:
        st.warning("Chưa nhập nội dung!")
    else:
        client = ElevenLabs(api_key=api_key)

        audio = client.text_to_speech.convert(
            voice_id=voice_map[voice_id],
            text=text,
            model_id="eleven_multilingual_v2"
        )

        output_file = "voice.mp3"

        # FIX đúng ở đây 👇
        audio_bytes = b"".join(audio)

        with open(output_file, "wb") as f:
            f.write(audio_bytes)

        st.success("✅ Xong!")

        st.audio(output_file)

        with open(output_file, "rb") as f:
            st.download_button("📥 Tải file", f, "voice.mp3")
