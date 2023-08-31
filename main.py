from pytube import YouTube
import moviepy.editor as mp
import requests
import os
import shutil
import argparse

def main(url=str,video_title=None,location=None):
    # Step 1: Download Audio from YouTube
    print("Fetching video information...")
    video = YouTube(url)
    audio_stream = video.streams.filter(only_audio=True).first()
    print(f"Downloading \"{audio_stream.title}\"... [{round(int(audio_stream.filesize) / (1024 ** 2),2)}mb]")
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
        video_title = audio_stream.title
    final_clip.write_videofile(f"{video_title}.mp4", codec="libx264", audio_codec="aac",fps=1)
    
    print("Cleaning up...")
    shutil.rmtree("temp/")

    return f"{location}/{video_title}.mp4"

# Handle getting the filename and url from the user!
if __name__ == "__main__":
    #Creates temp folder at startup, in case it doesn't already exist
    if not os.path.isdir("temp"):
        os.mkdir("temp")

    parser = argparse.ArgumentParser(description="Convert YouTube videos to ones with a static background whilist keeping the audio intact!")
    parser.add_argument('-u', '--url', help="The YouTube's video URL (default: ask at startup)", required=False, default=None)
    parser.add_argument('-n', '--name', help="The name of the final video file (default: video's title.mp4)", required=False, default=None)
    parser.add_argument('-l', '--location', help="Where should the video be located (default: at your current directory)", required=False, default=None)

    args = parser.parse_args()

    if not args.url:
        args.url = input("YouTube URL > ")

    #Passes all these to what does the magic :3
    main(url=args.url,video_title=args.name)
else:
    print("Musicfy is not meant to be imported, baaka!")
    #You're a sussy baka!
