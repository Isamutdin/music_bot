from aiogram.dispatcher.filters.state import StatesGroup, State


class Video(StatesGroup):
    video = State()
    mes = State()


class PlayList(StatesGroup):
    playlist = State()