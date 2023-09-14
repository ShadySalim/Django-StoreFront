from pytube import YouTube, Playlist
from moviepy.editor import *

def download_video(url, output_folder='videos'):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_folder)

def download_playlist(url, output_folder='videos'):
    playlist = Playlist(url)
    for video_url in playlist.video_urls:
        download_video(video_url, output_folder)

def video_to_audio(video_path, output_folder='audios'):
    video = VideoFileClip(video_path)
    audio = video.audio

    audio_folder = os.path.join(output_folder, os.path.dirname(os.path.basename(video_path)))
    os.makedirs(audio_folder, exist_ok=True)

    audio_path = os.path.join(audio_folder, os.path.splitext(os.path.basename(video_path))[0] + ".mp3")
    audio.write_audiofile(audio_path)

    video.reader.close()
    video.audio.reader.close_proc()

if __name__ == "__main__":
    # Example usage:
    video_url = 'https://www.youtube.com/watch?v=eoMqX4AAj7s'
    #playlist_url = 'https://www.youtube.com/playlist?list=your_playlist_id_here'

    # Download single video
    download_video(video_url)

    # Download playlist
    #download_playlist(playlist_url)

    # Convert video to audio
    video_path = 'videos/Video_Title.mp4'
    video_to_audio(video_path)
