from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, types
from state import Video, PlayList
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from pars import download_video, download_playlist
from os import remove

TOKEN = "1705450152:AAGnaIFa2xgob03m9dkD2Ja6QdDRL-fUyVA"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)







@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("У бота 2 комманды \n/video-Скачать видео\n/playlist-Скачать плэйлист")
    







###############################################################################
@dp.message_handler(commands="video")
async def state_v(message: types.Message):
    await message.answer("Просто отправте ссылки на видео с ютуба, а в конце написать комманду /end")
    await bot.delete_message(message.chat.id, message.message_id)
    await Video.video.set()

@dp.message_handler(state=Video.video, commands='end')
async def end_v(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)
    await state.finish()


@dp.message_handler(state=Video.video)
async def douwnload_v(message: types.Message):
    name = download_video(message.text)
    await bot.send_audio(message.chat.id, open(name, 'rb'))
    await bot.delete_message(message.chat.id, message.message_id)
    remove(name)
###############################################################################


###############################################################################
@dp.message_handler(commands="playlist")
async def state_pl(message: types.Message):
    await message.answer("Просто отправте ссылки на видео с ютуба, а в конце написать комманду /end")
    await bot.delete_message(message.chat.id, message.message_id)
    await PlayList.playlist.set()

@dp.message_handler(state=PlayList.playlist, commands='end')
async def end_pl(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)
    await state.finish()


@dp.message_handler(state=PlayList.playlist)
async def douwnload_pl(message: types.Message):
    names = download_playlist(message.text)
    for name in names:
        await bot.send_audio(message.chat.id, open(name, 'rb'))
        remove(name)
    
    await bot.delete_message(message.chat.id, message.message_id)
###############################################################################



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)