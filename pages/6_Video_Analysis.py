import openai

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64

from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import streamlit as st

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

client = OpenAI()
video = cv2.VideoCapture("data/videoanalysis.mp4")
video_file = open('videoanalysis.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)

base64Frames = []

while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release()

st.write(len(base64Frames), "frames read.")

# display_handle = display(None, display_id=True)
# for img in base64Frames:
#     st.image(img)
# img_data = base64.b64decode(frame.encode("utf-8"))
# display_handle.display(Image(data=img_data))
# im = Image.open(r"path to your image")  # r to convert it to a raw string
# im.show()
# display_handle.update(Image(data=base64.b64decode(img.encode("utf-8"))))
# time.sleep(0.025)

PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are frames from a video that I want to upload. Generate a compelling description that I can upload along with the video.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0:]),
        ],
    },
]
params = {
    "model": "gpt-4-vision-preview",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 200,
}

result = client.chat.completions.create(**params)
st.write(result.choices[0].message.content)

PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are frames of a video. Create a short voiceover script in the style of David Attenborough. Only include the narration.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0:]),
        ],
    },
]

params = {
    "model": "gpt-4-vision-preview",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 500,
}

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)

response = requests.post(
    "https://api.openai.com/v1/audio/speech",
    headers={
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
    },
    json={
        "model": "tts-1-1106",
        "input": result.choices[0].message.content,
        "voice": "onyx",
    },
)

audio = b""
for chunk in response.iter_content(chunk_size=1024 * 1024):
    audio += chunk

st.audio(audio)
