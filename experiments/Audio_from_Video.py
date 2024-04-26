import openai

import shutil
import cv2  # To import use !pip install opencv-python
import base64

from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import streamlit as st
from pytube import YouTube
import moviepy.editor as mp

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

st.set_page_config(page_title="Audio from video")
st.header("Extract audio from video🎥📷")

client = OpenAI()


def extract_audio(v_p):
    # Load the video file
    video = mp.VideoFileClip(v_p)

    # Extract the audio
    audio = video.audio

    # Write the audio to a file
    audio.write_audiofile("audio.mp3")
    st.audio("audio.mp3")
    return audio


with st.form("audio_from_video"):
    st.write("NOTE: This is only for demo purpose and not for industrial usage for now. To avoid heavy charges keep "
             "video link <= 2mins.")
    video_link = st.text_input("Enter video link.", value="https://www.youtube.com/watch?v=d95PPykB2vE")
    submit = st.form_submit_button("Start")
    path = r"./pages/video"
    if submit:
        video_read_path = "./pages/video/video_analysis.mp4"
        st.video(video_link)
        extract_audio(video_read_path)
