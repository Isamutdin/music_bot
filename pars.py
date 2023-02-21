from pytube import YouTube
from pytube import Playlist
import requests

DOMEN = 'http://127.0.0.1:8000/'
API = 'api/v1/videoYT/'
APIUSER = 'api/v1/uservideoYT/'

def check_videoYT(yt_id):
    data = {'yt_id': yt_id}
    r = requests.get(DOMEN+API, data=data).json()['video_id']
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
    r = requests.post(DOMEN+API, data=info).json()
    info['video'] = r['video']
    requests.post(DOMEN+APIUSER, data=info)
    return 'ok'


def download_playlistYT(url):
    pl = Playlist(url)
    spisok = []
    for video in pl.videos:
        spisok.append(video.streams.filter(mime_type="audio/mp4").first().download(r'F:\music_bot\audio'))
    return spisok





if __name__ == "__main__":
    #5208514073:AAE4tGvLhsCeWAaR1Cuv8C30YSScqvuyuXk
    #1770295162
    #1705450152
    #1063089542 - Саня
    #585067098 - Катя
    #692175727 - Матвей
    # url = 'https://www.youtube.com/watch?v=oGT3Z7fVNc0'
    # spsiok_urlYT = ['https://www.youtube.com/watch?v=ybgWXT768pA&list=RDMMjqdGiHPMy_c&index=7', 'https://www.youtube.com/watch?v=8uDftl_TJzY&list=RDMMjqdGiHPMy_c&index=10']
    # for elem in spsiok_urlYT:
    #     data = {
    #         'token': '34wetaq35fc1243q',
    #         'url': elem, #'https://www.youtube.com/watch?v=1YBpZBE3c2U&list=RDMMjqdGiHPMy_c&index=9', #'https://www.youtube.com/watch?v=XWJ1sn3QC2c',
    #         'video_id':'CQACAgIAAxkDAAIKPWPvr1LxFSo-jVTqDw3h1TWyhviHAAI_IgACEYaBS5iVU8c4PZoRLgQ',
    #         'title':'wercvzxvgz',
    #         'url_img':'http://img.youtube.com/vi/fJc3WBiWEos/mqdefault.jpg',
    #         'author': 'Swap',
    #     }
    data = {'token': '', 'url': 'https://youtube.com/watch?v=fC1HF29n9UA', 'title': 'DVRST, OBLXKQ - ENDLESS LOVE', 'url_img': 'http://img.youtube.com/vi/fC1HF29n9UA/mqdefault.jpg', 'author': 'DVRST', 'yt_id': 'fC1HF29n9UA', 'video_id': 'CQACAgIAAxkDAAILvGP1JxrLiGMR-1ugWuf5t71-NDsyAALyJgACPyqpS1U06JX96hR1LgQ', 'telegram_id': 1770295162}
    r = (requests.post('http://127.0.0.1:8000/api/v1/videoYT/', data=data).json())
    print(r)
    data['video']= r['video']
    print(requests.post(DOMEN+APIUSER, data=data).text)
    # data = {
    #     'audio': 'CQACAgIAAxkDAAIKLGPvq6fx9KFF2Tkla6GHnD3081dlAAL0IQACEYaBSw_w0_wwEGihLgQ',
    #     'chat_id': '1705450152',
    # }
    # print(requests.post('https://api.telegram.org/bot1705450152:AAGnaIFa2xgob03m9dkD2Ja6QdDRL-fUyVA/sendAudio', data=data).text)
    # yt = YouTube('https://www.youtube.com/watch?v=fJc3WBiWEos')
    # v = yt.streams.filter(mime_type="audio/mp4").first().download(r'F:\music_bot\audio')
    # print(yt.author, yt.watch_url)
    