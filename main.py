from pytube import YouTube
import moviepy.editor as mp
import requests
import sys
import os
import shutil

def main(url=str,video_title=None):
    # Step 1: Download Audio from YouTube
    video = YouTube(url)

    audio_stream = video.streams.filter(only_audio=True).first()
    audio_stream.download(output_path="temp", filename="music.mp3")

    # 1.5: Get Thumbnail
    response = requests.get(video.thumbnail_url)
    with open('temp/thumbnail.jpg', 'wb') as f:
        f.write(response.content)

    # Step 2: Combine Audio with Image using MoviePy
    audio_clip = mp.AudioFileClip("temp/music.mp3")
    image_clip = mp.ImageClip("temp/thumbnail.jpg").set_duration(audio_clip.duration)
    final_clip = image_clip.set_audio(audio_clip)
    if not video_title:
        video_title = "output_video"
    final_clip.write_videofile(f"{video_title}.mp4", codec="libx264", audio_codec="aac",fps=1)
    print("Cleaning up...")
    shutil.rmtree("temp/")

# Handle getting the filename and url from the user!
if __name__ == "__main__":

    #Creates temp folder at startup, in case it doesn't already exist
    if not os.path.isdir("temp"):
        os.mkdir("temp")

    #Sets variables so Python doesn't bitch about them
    title = None
    url = None

    #URL
    try:
        url = sys.argv[1]
    except IndexError:
        url = input("YouTube URL > ")
    
    #Title
    try:
        title = sys.argv[2]
    except IndexError:
        title = input("Filename (Optional) > ")
    
    #Passes all these to what does the magic :3
    main(url,video_title=title)
else:
    print("Musicfy is not meant to be imported, baaka!")
    #You're a sussy baka!