import time

import os
import requests

from PIL import Image
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
stability_api = os.environ['STABILITY_API_KEY']
st.subheader("Image to Video using StabilityAI")
st.markdown(":blue[NOTE: We are using StabilityAI - https://platform.stability.ai/docs/api-reference#tag/Image-to-Video \n]")


def generate_image_function(image_file_name):
    img_response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
            "authorization": f"Bearer {stability_api}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": f"{prompt}",
            "output_format": "png",
        },
    )
    if img_response.status_code == 200:
        with open(f"./{image_file_name}.png", 'wb') as file:
            img = img_response.content
            file.write(img)
            st.image(img)
    else:
        raise Exception(str(img_response.json()))


def generate_id_fn(image_file_name):
    response = requests.post(
        f"https://api.stability.ai/v2beta/image-to-video",
        headers={
            "authorization": f"Bearer {stability_api}"
        },
        files={
            "image": open(f"./{image_file_name}.png", "rb")
        },
        data={
            "seed": 0,
            "cfg_scale": 1.8,
            "motion_bucket_id": 127
        },
    )

    generation_id = response.json().get('id')
    print("Generation ID:", generation_id)
    st.write(generation_id)
    # st.write(len(generation_id))
    return generation_id


def generate_video_stability(generation_id):
    print("GENERATED_ID: In video creation" + generation_id)
    response = requests.request(
        "GET",
        f"https://api.stability.ai/v2beta/image-to-video/result/{generation_id}",
        headers={
            'accept': "video/*",  # Use 'application/json' to receive base64 encoded JSON
            'authorization': f"Bearer {stability_api}"
        },
    )

    if response.status_code == 202:
        print("Generation in-progress, try again in 10 seconds.")
    elif response.status_code == 200:
        print("Generation complete!")
        with open("../experiments/video.mp4", 'wb') as file:
            video_file = response.content
            file.write(video_file)
            st.video(video_file)
    else:
        raise Exception(str(response.json()))


def resize_image(image, width, height):

    # Get the current width and height of the image.
    current_width, current_height = image.size

    # Calculate the ratio between the desired dimensions and the current dimensions.
    width_ratio = width / current_width
    height_ratio = height / current_height

    # Resize the image using the calculated ratio.
    resized_image = image.resize((int(width_ratio * current_width), int(height_ratio * current_height)))

    return resized_image


def test_resize_image(file_name):
    # Load the image.
    # f_name = f".{file_name}"
    # print(f_name)
    image = Image.open(file_name + ".png")

    # Resize the image to 400x400 pixels.
    resized_image = resize_image(image, 1024, 576)

    # Save the resized image.
    resized_image.save("resized_image.png")


def show_video(generation_id):
    generated_id = st.text_input(label="generated id", value=generation_id)
    submit_button = st.form_submit_button("Generate Video")
    if submit_button:
        generate_video_stability(generated_id)


def countdown(seconds):
    while seconds > 0:
        st.write(seconds)
        seconds -= 1
        time.sleep(1)


with st.form("get_image_input"):
    prompt = st.text_input("Enter prompt for image generation")
    file_name = st.text_input("Enter file name to save file")
    submit = st.form_submit_button("Generate Image")
    if submit:
        generate_image_function(file_name)
        test_resize_image(file_name)
        generation_id = generate_id_fn("resized_image")
        # generation_id = "27711eb72c3f0f8cd29609c6511c61582cf43d41967c79a39d55d25da1fa93f6"
        st.text_input("3ed88784ad0f6d57565fe020cb2bc8f84069194c08ddebaedd94d2b15e6ab623", value=generation_id)
        generate_video_stability(generation_id)
        # with open("video.mp4", 'wb') as file:
        #     video_file = response.content
        #     file.write(video_file)
        st.video("video.mp4")
        # countdown(10)
        # generate_video_stability(generation_id)

        # if response.status_code == 200:
        #     with open(f"./{file_name}.png", 'wb') as file:
        #         img = response.content
        #         file.write(img)
        #         st.image(img)
        # else:
        #     raise Exception(str(response.json()))
