import streamlit as st
import pandas as pd
import math
from pathlib import Path
from utils import analyze_intonation

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Music Education Simplified',
    page_icon='🎤', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.
  # in megabytes

# Title and description
st.title("🎤 Vocal Intonation Analyzer")
st.markdown(
    """
    Upload a vocal recording and receive feedback on pitch stability and intonation accuracy.
    This tool is part of a broader music education initiative to assist learners and teachers
    in evaluating performance quality.
    """
)

# Upload audio
uploaded_file = st.file_uploader("Upload a singing recording (.wav or .mp3)", type=["wav", "mp3"])

if uploaded_file:
    with open("temp.wav", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Analyzing..."):
        feedback, plot_path = analyze_intonation("temp.wav")

    st.image(plot_path, caption="Pitch KDE (wrapped to one octave)")
    st.success(feedback)