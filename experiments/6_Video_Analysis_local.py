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

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

st.set_page_config(page_title="Video Analysis")
st.header("Video Analysis🎥📷")


def download_video_from_youtube(link, save_path):
    yt = YouTube(link)
    yt_video = yt.streams.get_highest_resolution()
    # download the video
    yt_video.download(save_path)


def delete_files(folder_path):
    files = os.listdir(folder_path)

    if not files:
        print("The folder is empty")
    else:
        for file in files:
            os.remove(os.path.join(folder_path, file))
            print("All files in the folder have been deleted")


def rename_file():
    # Get the path to the folder
    folder_path = r"./pages/video"

    # Get a list of all the files in the folder
    files = os.listdir(folder_path)

    # Get the first file in the list
    first_file = files[0]

    # Get the new file name
    new_file_name = "video_analysis.mp4"

    # Rename the file
    os.rename(os.path.join(folder_path, first_file), os.path.join(folder_path, new_file_name))
    src = folder_path + "/" + new_file_name
    print(src)
    dst = r"./"
    # shutil.copyfile(src, dst)
    # 2nd option
    shutil.copy2(src, dst)  # dst can be a folder; use shutil.copy2() to preserve timestamp


def video_analysis(base64frames, fc):
    prompt = "These are frames from a video that I want to upload." + " Check the video frames and answer the question: \"" + user_question + "\" If you don't find answer after going through all frames from the video then revert back with - UNABLE TO FIND IN VIDEO."
    # print(prompt)

    PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": [
                prompt,
                *map(lambda x: {"image": x, "resize": 768}, base64frames[0::fc]),
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


def audio_generation(base64frames, fc):
    PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": [
                "These are frames of a video. Create a short voiceover script in english. Only include the narration.",
                *map(lambda x: {"image": x, "resize": 768}, base64frames[0::fc]),
            ],
        },
    ]

    params = {
        "model": "gpt-4-vision-preview",
        "messages": PROMPT_MESSAGES,
        "max_tokens": 1500,
    }

    result = client.chat.completions.create(**params)
    st.title("Audio content")
    st.write(result.choices[0].message.content)

    with st.spinner("Loading content..."):
        response = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {openai.api_key}",
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


def read_video_file(v_file):
    base64frames = []

    with st.spinner("Working"):
        while v_file.isOpened():
            success, frame = v_file.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            base64frames.append(base64.b64encode(buffer).decode("utf-8"))

        v_file.release()
        frameCounts = len(base64frames)
        st.write(frameCounts, "frames read.")
        return base64frames, frameCounts





client = OpenAI()

with st.form("Video_analysis"):
    st.write("NOTE: This is only for demo purpose and not for industrial usage for now. To avoid heavy charges keep "
             "video link <= 2mins.")
    video_link = st.text_input("Enter video link.", value="https://www.youtube.com/watch?v=d95PPykB2vE")
    submit = st.form_submit_button("Start")
    path = r"./pages/video"
    if submit:
        delete_files(path)
        download_video_from_youtube(video_link, path)
        rename_file()
        video_read_path = "./pages/video/video_long.mp4"
        video = cv2.VideoCapture(video_read_path)
        video_file = open(video_read_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        read_video_file(video)

        # exit()
        # display_handle = display(None, display_id=True)
        # for img in base64Frames:
        #     st.image(img)
        # img_data = base64.b64decode(frame.encode("utf-8"))
        # display_handle.display(Image(data=img_data))
        # im = Image.open(r"path to your image")  # r to convert it to a raw string
        # im.show()
        # display_handle.update(Image(data=base64.b64decode(img.encode("utf-8"))))
        # time.sleep(0.025)

with st.form("GetVideoURL"):
    user_question = st.text_area("Ask anything related to the video", value="Who is girl in the video?")
    get_answer = st.form_submit_button("Get Answer")
    if get_answer:
        video_read_path = "./pages/video/video_long.mp4"
        video = cv2.VideoCapture(video_read_path)
        video_file = open(video_read_path, 'rb')
        video_bytes = video_file.read()
        base64Frames, frame_counts = read_video_file(video)
        video_analysis(base64Frames, frame_counts)
        audio_generation(base64Frames, frame_counts)
