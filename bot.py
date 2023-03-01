from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from state import Video, PlayList
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from pars import *
from os import remove


with open("TOKEN.txt", 'r') as f: 
    TOKEN = f.read()

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("У бота 2 комманды \n/video-Скачать видео\n/playlist-Скачать плэй лист")
    print(message)

###############################################################################
@dp.message_handler(commands="video")
async def state_v(message: types.Message):
    r = await message.answer("Просто отправь ссылки на видео с ютуба, а в конце написать комманду /end")
    await message.delete()
    await Video.video.set()

@dp.message_handler(state=Video.video, commands='end')
async def end_v(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()

@dp.message_handler(state=Video.video)
async def douwnload_v(message: types.Message):
    await message.delete()
    r = check_videoYT(message.text)
    if r:
        await bot.send_audio(message.chat.id, r)
    else:
        name, info = download_videoYT(message.text)
        result = await bot.send_audio(message.chat.id, open(name, 'rb'))
        info['video_id'] = result.audio.file_id
        info['telegram_id'] = message.from_id
        remove(name)
        create_videoYT(info)
###############################################################################


###############################################################################
@dp.message_handler(commands="playlist")
async def state_pl(message: types.Message):
    await message.answer("Просто отправь ссылки на видео с ютуба, а в конце написать комманду /end")
    await message.delete()
    await PlayList.playlist.set()

@dp.message_handler(state=PlayList.playlist, commands='end')
async def end_pl(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()

@dp.message_handler(state=PlayList.playlist)
async def douwnload_pl(message: types.Message):
    await message.delete()
    r = check_playlistYT(message.text)
    if r:
        async for tg_id in r:
            await bot.send_audio(message.from_id, audio=tg_id[0])
    else:
        generator, playlist = create_playlist(message.text, message.from_id)
        for video in generator:
            if isinstance(video, str):
                await bot.send_audio(message.from_id, video)
            else:
                f, info = video
                v = await bot.send_audio(message.from_id, open(f, 'rb'))
                info['video_id'] = v.audio.file_id
                info['telegram_id'] = message.from_id
                r = create_videoYT(info)
                remove(f)
                requests.post(DOMEN+APIVIDEOPLAYLIST, data={'playlist': playlist, 'video': r}).text
    
###############################################################################
    



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    