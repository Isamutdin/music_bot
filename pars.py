from os import remove
import random
from pytube import YouTube
from pytube import Playlist
import requests

DOMEN = 'http://127.0.0.1:8000/'
APIVIDEOYT = 'api/v1/videoYT/'
APIPLAYLIST = 'api/v1/playlistYT/'
APIUSERPLAYLIST = 'api/v1/userplaylistYT/'
APIVIDEOPLAYLIST = 'api/v1/videoplaylistYT/'
APIUSERVIDEO = 'api/v1/uservideoYT/'

def check_videoYT(yt_id):

    yt_id= YouTube(f"https://www.youtube.com/watch?v={yt_id}")

    data = {'yt_id': yt_id.video_id}
    r = requests.get(f"{DOMEN}{APIVIDEOYT}", data=data).json()['video_id']

    if r != 'None': return r
    return False

def download_videoYT(url):
    yt = YouTube(url)
    info = {
        'token': "",
        'url': yt.watch_url,
        'title': yt.title,
        'url_img': f'http://img.youtube.com/vi/{yt.video_id}/mqdefault.jpg',
        'author': yt.author,
        'yt_id': yt.video_id
    }

    return yt.streams.filter(mime_type="audio/mp4").first().download(r'F:\music_bot\audio'), info

def create_videoYT(info):
    r = requests.post(DOMEN+APIVIDEOYT, data=info).json()

    info['video'] = r['video']
    r = requests.post(DOMEN+APIUSERVIDEO, data=info)
    return info['video']

def check_playlistYT(url):
    pl = Playlist(url)
    data = {'yt_id': pl.playlist_id}
    r = requests.get(DOMEN+APIPLAYLIST, data=data).json()
    if r != 'None': return r
    return False

def download_playlistYT(generator):
    for video in generator:
        r = check_videoYT(video.video_id)
        if r: yield r
        yield download_videoYT(video.watch_url)

def create_playlist(url, from_id):
    pl = Playlist(url)

    info = {
        'url': pl.playlist_url,
        'url_img': 'https://www.youtube.com/playlist?list=PLOwSo8kHs4XR447QoOO4csKctRnCYOvvR',
        'title': pl.title,
        'author': pl.owner,
        'yt_id': pl.playlist_id,
    }

    create_plalist = requests.post(DOMEN+APIPLAYLIST, data=info).json()['playlist']
    requests.post(DOMEN+APIUSERPLAYLIST, data={'playlist': create_plalist, 'telegram_id': from_id}).text

    return download_playlistYT(pl.videos_generator()), create_plalist



if __name__ == "__main__":
    

    print(download_videoYT('https://www.youtube.com/watch?v=Onw-MslOkSU'))
