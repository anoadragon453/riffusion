import io

import streamlit as st

from riffusion.streamlit import util as streamlit_util


def render_split_audio() -> None:
    st.set_page_config(layout="wide", page_icon="🎸")

    st.subheader(":scissors: Audio Splitter")
    st.write(
        """
    Split an audio into stems of {vocals, drums, bass, other}.
    """
    )

    device = streamlit_util.select_device(st.sidebar)
    splitter = streamlit_util.get_audio_splitter(device=device)

    audio_file = st.file_uploader(
        "Upload audio",
        type=["mp3", "m4a", "ogg", "wav", "flac"],
        label_visibility="collapsed",
    )

    if not audio_file:
        st.info("Upload audio to get started")
        return

    st.write("#### original")
    st.audio(audio_file)

    if not st.button("Split", type="primary"):
        return

    segment = streamlit_util.load_audio_file(audio_file)

    # Split
    stems = splitter.split(segment)

    # Display each
    for name, stem in stems.items():
        st.write(f"#### {name}")
        audio_bytes = io.BytesIO()
        stem.export(audio_bytes, format="mp3")
        st.audio(audio_bytes)


if __name__ == "__main__":
    render_split_audio()
