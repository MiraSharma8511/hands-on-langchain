import os

from dotenv import load_dotenv
from pexelsapi.pexels import Pexels
import streamlit as st

load_dotenv()
api = os.environ['PEXELS_API_KEY']
print(api)

pexel = Pexels(api)
# get_photo = pexel.get_photo(get_id=0)
# st.image(get_photo)
search_photos = pexel.search_photos(query='ocean', orientation='', size='', color='', locale='', page=1, per_page=15)
# print("_______________________________________________________________________________________________________________")
# print(len(search_photos))
# print("_______________________________________________________________________________________________________________")
# print(search_photos)
# print("_______________________________________________________________________________________________________________")
for i in range(len(search_photos)):
    st.image(search_photos['photos'][i]['src']['original'])
# print(search_photos.photos[0].photographer_url)
# print(get_photo)
#
search_videos = pexel.search_videos(query='ocean', orientation='', size='', color='', locale='', page=1, per_page=15)
# print(search_videos)
print("_______________________________________________________________________________________________________________")
# for i in range(len(search_videos)):
# video_links = [video['link'] for video in search_videos['video_files']]
# print(video_links)
video_url = search_videos['videos']
# print(len(video_url))
for i in range(len(video_url)):
    print("_______________________________________________________________________________________________________________\n")
    # for j in range(len(video_url[i]['video_files'])):
    video_link = (video_url[i]['video_files'][0]['link'])
    st.video(video_link)

# st.video(video_url)
# st.video(search_videos)
