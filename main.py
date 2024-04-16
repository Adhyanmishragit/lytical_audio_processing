import streamlit as st
import tempfile
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Google API for audio processing
google_api_key = os.getenv("GOOGLE_API_KEY")


def configure_genai():
    st.session_state.app_key = google_api_key
    try:
        genai.configure(api_key=st.session_state.app_key)
    except AttributeError as e:
        st.warning(e)


def process_audio(audio_file_path, prompt):
    """Process the audio using the user's prompt with Google's Generative API."""
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    audio_selected = genai.upload_file(path=audio_file_path)
    response = model.generate_content(
        [
            prompt,
            audio_selected
        ]
    )
    return response.text


def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary file and return the path."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error handling uploaded file: {e}")
        return None


def main():
    configure_genai()

    page_icon_path = "img/logo.png"
    if os.path.exists(page_icon_path):
        st.set_page_config(
            page_title="Lytical Audio Processor",
            page_icon=page_icon_path,
        )

    st.header("🎧 Lytical Audio Processor 🗣️")

    st.sidebar.image("img/audio_ai_speak.jpeg")
    st.sidebar.write("---")

    st.sidebar.title("🎧 Audio File's Section")
    audio_file = st.sidebar.file_uploader("Upload your Audio file \nto be processed", type=['wav', 'mp3'])

    if st.sidebar.button("Reset Data", use_container_width=True, type="primary"):
        st.rerun()

    st.sidebar.write("---")
    st.sidebar.image("img/audio_ai.jpeg")
    st.sidebar.write("Developed by @CodeLytical")

    user_prompt = st.text_input("Enter your custom AI prompt:", placeholder="E.g., 'Please summarize the audio:'")
    st.write("")

    if audio_file is not None:
        audio_path = save_uploaded_file(audio_file)
        st.audio(audio_path)

        if st.button(' Process Audio ', args={"button_color": "red"}, type="primary"):
            with st.spinner('Lytical processing...'):
                if not user_prompt.strip():
                    # Set a default prompt
                    default_prompt = "Please process this audio and give me detailed information."
                    st.warning(f"No prompt provided. Using default prompt: '{default_prompt}'")
                    processed_text = process_audio(audio_path, default_prompt)
                else:
                    processed_text = process_audio(audio_path, user_prompt)
                st.info(processed_text)


if __name__ == "__main__":
    main()