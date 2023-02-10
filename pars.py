from pytube import YouTube
from pytube import Playlist


def download_video(url):
    yt = YouTube(url)
    return yt.streams.filter(mime_type="audio/mp4").first().download()


def download_playlist(url):
    pl = Playlist(url)
    spisok = []
    for video in pl.videos:
        spisok.append(video.streams.filter(mime_type="audio/mp4").first().download())
    return spisok






if __name__ == "__main__":
    url = 'https://www.youtube.com/playlist?list=PLqGS6O1-DZLo8fjcztVUM0Eotb1fT2ZOh'
    print(download_playlist(url))