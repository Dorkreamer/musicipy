from pytube import YouTube
import moviepy.editor as mp
import requests
import os
import shutil
import argparse
import re

def main(url=str,video_title=None,location=None):
    try:
        #Get the real url in case it's going through a redirect
        url = requests.get(args.url).url

        # Download Audio from YouTube
        print("Fetching video information...")
        video = YouTube(url)
        audio_stream = video.streams.filter(only_audio=True).first()
        print(f"Downloading \"{audio_stream.title}\"... [{round(int(audio_stream.filesize) / (1024 ** 2),2)}mb]")
        audio_stream.download(output_path="temp", filename="music.mp3")

        # Download Thumbnail
        response = requests.get(video.thumbnail_url)
        if response.status_code == 200:
            with open('temp/thumbnail.jpg', 'wb') as f:
                f.write(response.content)
        else:
            print(f"Error! YouTube returned {response.status_code}")
            a = input("Do you want to retry?")
            if a.lower() == "y":
                response = requests.get(video.thumbnail_url)
                if response.status_code == 200:
                    with open('temp/thumbnail.jpg', 'wb') as f:
                        f.write(response.content)
                else:
                    print(f"Error downloading thumbnail, {response.status_code}")
            else:
                exit()

        # Mash both together using MoviePy
        audio_clip = mp.AudioFileClip("temp/music.mp3")
        image_clip = mp.ImageClip("temp/thumbnail.jpg").set_duration(audio_clip.duration)
        final_clip = image_clip.set_audio(audio_clip)
        if not video_title:
            video_title = audio_stream.title
        
        # Clean filename
        video_title = re.sub(r'[\\/:*?"<>|]',"",video_title)

        if not location:
            location = os.getcwd()

        final_clip.write_videofile(f"{location}/{video_title}.mp4", codec="libx264", audio_codec="aac",fps=1)
        
        #Cleans up
        print("Cleaning up...")
        shutil.rmtree("temp/")

        #Returns the file path, for usage within scripts
        return f"{location}/{video_title}.mp4"
    except Exception as e:
        print(e)
        a = input("An error as occurred! Do you want to try again? ")
        if a.lower() == "y":
            try:
                main(url,video_title,location)
            except Exception as e:
                print("An error has occurred, and musicipy cannot proceed...")
                exit()
        else:
            exit()

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
