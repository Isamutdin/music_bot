from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from state import Video, PlayList
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from pars import download_videoYT, download_playlistYT, check_videoYT, create_videoYT
from os import remove

#keyboard = types.ReplyKeyboardRemove(True)


with open("TOKEN.txt", 'r') as f: 
    TOKEN = f.read()


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("У бота 2 комманды \n/video-Скачать видео\n/playlist-Скачать плэй лист")

###############################################################################
@dp.message_handler(commands="video")
async def state_v(message: types.Message):
    r = await message.answer("Просто отправь ссылки на видео с ютуба, а в конце написать комманду /end")
    print(message)
    await message.delete()
    await Video.video.set()

@dp.message_handler(state=Video.video, commands='end')
async def end_v(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()

@dp.message_handler(state=Video.video)
async def douwnload_v(message: types.Message):
    url = message.text.split("&")[0].replace("www.", '')
    r = check_videoYT(url.split("/")[-1])
    if r:
        await bot.send_audio(message.chat.id, r)

    else:
        name, info = download_videoYT(message.text)
        result = await bot.send_audio(message.chat.id, open(name, 'rb'))
        info['video_id'] = result.audio.file_id
        info['telegram_id'] = message.from_id
        remove(name)
        create_videoYT(info)
    await message.delete()
###############################################################################


###############################################################################
# @dp.message_handler(commands="playlist")
# async def state_pl(message: types.Message):
#     await message.answer("Просто отправь ссылки на видео с ютуба, а в конце написать комманду /end")
#     await message.delete()
#     await PlayList.playlist.set()

# @dp.message_handler(state=PlayList.playlist, commands='end')
# async def end_pl(message: types.Message, state: FSMContext):
#     await message.delete()
#     await state.finish()

# @dp.message_handler(state=PlayList.playlist)
# async def douwnload_pl(message: types.Message):
#     names = download_playlistYT(message.text)
#     for name in names:
#         cap = name.split("\\")[-1][:-4]
#         await bot.send_audio(message.chat.id, open(name, 'rb'), caption=cap, title=cap)
#         remove(name)

#     await message.delete()
###############################################################################
    



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    