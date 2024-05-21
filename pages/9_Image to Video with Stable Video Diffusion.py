import requests
import os
import requests

import streamlit as st
from IPython.core.display import Video

st.subheader("Image to Video using Stable Video Diffusion")
st.markdown(":blue[NOTE: We tried running the same code on local machine but machine need to have NVIDIA Graphic card "
            "as Pytorch doesn't support Intel Graphic card."
            "In such case, I would suggest using Google Colab as it provides Free GPU and code runs faster than "
            "local. (If your machine is having NVIDIA Graphics you try running it locally.) \n]")
st.write("\n Check Notebook here... 👇👇 \n\n")
st.link_button(label=":grey[Colab Notebook - Image-to-Video using StableVideoDiffusion.ipynb]",
               url="https://colab.research.google.com/drive/1lmv0O_pBYZNKozNDymLts8-Eyb0sjeHD")
st.divider()
st.subheader("How to do it?")
st.write("Install requirements")

code1 = ("!pip install diffusers \n"
         "!pip install request \n"
         "!pip install streamlit \n"
         "!pip install accelerate \n")
st.code(code1, language='python')

code2 = """import torch
from diffusers.utils import load_image, export_to_video
from diffusers import DiffusionPipeline, StableVideoDiffusionPipeline
from IPython.display import Image, Video

# pipeline = DiffusionPipeline.from_pretrained("stabilityai/stable-video-diffusion-img2vid-xt")

pipeline = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt", torch_dtype=torch.float16, variant="fp16"
)
pipeline.enable_model_cpu_offload()
image_url="https://ibb.co/4VqvzJL"
dis_image = Image(image_url)
display(dis_image)
image = load_image(image_url)
image = image.resize((1024, 576))
generator = torch.manual_seed(42)
frames = pipeline(image, decode_chunk_size=8, generator=generator).frames[0]
export_to_video(frames, "generated.mp4", fps=7)"""
st.code(code2, language='python')
st.image("https://i.ibb.co/MCvwr9H/rocket.png")

code3 = """video = Video(filepath = "./generated.mp4", format = "mp4")
display(video)"""
st.write("Explain Code")
st.code(code3, language='python')
st.video("./Rocket-Video.mp4")

st.write("Reference - https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt")


