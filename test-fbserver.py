from gradio_client import Client
import requests
import threading
from gradio_client import Client
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
from pydub import AudioSegment

server_list = [
    "https://facebook-musicgen.hf.space/",
]
def getMusic(server_name, emotion):
    client = Client(server_name)
    result = client.predict(
        emotion,  # str  in 'Describe your music' Textbox component
        "",
        # str (filepath or URL to file) in 'File' Audio component
        fn_index=0
    )
    return result[0] # chỉ lấy mp4 thôi ko lấy wav


def save_to_server(mp4_link, emotion, stt):
    url = "https://un-silent-backend-develop.azurewebsites.net/api/v1/generated-musics"
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    }

    # Dữ liệu yêu cầu
    data = {
        "Emotion": emotion,
    }

    files = {
        "MusicFile": (f"{emotion}{stt}.mp4", open(mp4_link, "rb")),
    }

    # Gửi yêu cầu POST
    response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code == 200:
        print("Save to server successfully")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def process_server(server_name, emotion, stt):
    print(f"Gen nhạc với emotion {emotion} trên server {server_name}")
    music = getMusic(server_name, emotion)
    # duplicate_music = duplicate(music, emotion)
    save_to_server(music, emotion, stt)
    print(music)
    stt += 1
    print("-------------------------------------------")



def duplicate(input_video_path, emotion):
    clip = VideoFileClip(input_video_path)

    num_duplicates = 4

    video_clips = [clip] * num_duplicates

    # Ghép các đoạn video lại với nhau
    final_clip = video_clips[0]
    for i in range(1, num_duplicates):
        final_clip = crossfade(final_clip, video_clips[i])

    # # Lưu video ghép 60s xuống đĩa
    output_path = "putput.mp4"
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

def crossfade(video1, video2, fade_duration=3.0):
    clip1 = VideoFileClip(video1)
    clip2 = VideoFileClip(video2)

    fade_duration = min(fade_duration, clip1.duration, clip2.duration)

    clip1 = clip1.fade_out(fade_duration)
    clip2 = clip2.fade_in(fade_duration)

    final_clip = concatenate_videoclips([clip1, clip2])
    return final_clip


if __name__ == "__main__":
    stt = 1
    # emotion = input("Vui lòng chọn loại emotion muốn gen: \n 1. anger, 2. disgust, 3. fear, 4. joy, 5. neutral, 6. sadness, 7. surprise \n")

    map = {
        1: "anger",
        2: "disgust",
        3: "fear",
        4: "joy",
        5: "neutral",
        6: "sadness",
        7: "surprise",
    }

    while True:
        for i in range(1, 8):
            emotion = map[i]
            process_server(server_list[0], emotion, stt)



