from aiogram import __version__ as vers; print(vers)

# --------------- IMPRT ---------------

from aiogram.filters.content_types import ContentTypesFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types
from random import choice, shuffle
from aiogram import Router, F
from generators import *
from buttons import *

from aiogram.filters.callback_data import CallbackData

import asyncio
import logging
import config
import data

# --------------- ADMIN ---------------

logging.basicConfig(level=logging.INFO)
bot = Bot(config.TOKEN)
dp = Dispatcher()

# --------------- OPRDS ---------------

month_cycle_gen()
    
# --------------- STATE ---------------

class DocsDownloadState(StatesGroup):
    data_state         = State()
    lesson_state       = State()
    docs_state         = State()
    down_state         = State()
    accepting_state    = State()


class CheckWords(StatesGroup):
    start              = State()
    checking           = State()
    accepting          = State()


class Check(StatesGroup):
    check              = State()

# --------------- FUNCS ---------------

async def cmd_start(message : types.Message, state : FSMContext):
    await state.clear()
    await message.answer("Привет,\nЯ - бот Конспектик\nПерейдём к командам:", reply_markup=keyboardGen(buttons_commands))
    await state.set_state(Check.check)


async def cmd_check(message : types.Message, state : FSMContext):
    text = message.text
    await state.clear()

    if "Найти" in text: # Доделать
        pass
    
    if "Загрузить" in text:
        await message.answer("К какому уроку относится этот коспект?", reply_markup=keyboardGen(buttons_lesson))
        await state.set_state(DocsDownloadState.data_state)
        
    if "Тест" in text:
        await message.answer("К какому уроку тест?",
                             reply_markup=keyboardGen(buttons_test_choice))
        await state.set_state(CheckWords.checking)



async def cmd_data(message : types.Message, state : FSMContext):
    await state.update_data(ch_lesson=message.text.lower())
    await message.answer("В какой день недели?", reply_markup=keyboardGen(buttons_days))
    await state.set_state(DocsDownloadState.docs_state)


async def cmd_docs(message : types.Message, state : FSMContext):
    await state.update_data(ch_data=message.text.lower())
    await message.answer("Прикрепите файлы, которые хотите загрузить", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(DocsDownloadState.down_state)
    


async def cmd_down(message : types.Message, state : FSMContext):
    user_data = await state.get_data()

    file_id = message.document.file_id
    name = message.document.file_name
    
    repl = f"{user_data['ch_lesson']}, {user_data['ch_data']}"
    print(repl)
    
    file = await bot.get_file(file_id)
    file_path = f"documents/"
    await bot.download_file(file_path, naming(name, repl))
    await message.answer("Это всё?", reply_markup=keyboardGen(buttons_adding))
    await state.clear()

    

async def cmd2_checking(message : types.Message, state : FSMContext):
    
    try:
        print(1)
        naming = await state.get_data()
        word = naming["text"]
    except:
        print(2)
        await state.update_data(test=config.AVAILABLE_TESTS[message.text])
        await state.update_data(text="")
        naming = await state.get_data()
        word = naming["text"]
    print(3)
    words = naming["test"]
    text, plumbum = converter(word, words, message.text)
    
    await state.update_data(text=text)
    await message.answer(plumbum + text, reply_markup=testKeyboard(words, text))
    await state.set_state(CheckWords.checking)
    

# --------------- REGST ---------------

dp.message.register(cmd_start, Command(commands=['start', "return", "exit", "clear", "cls", "cancel"]))
dp.message.register(cmd_check, Check.check)

dp.message.register(cmd_data, DocsDownloadState.data_state)
dp.message.register(cmd_docs, DocsDownloadState.docs_state)
dp.message.register(cmd_down, DocsDownloadState.down_state, ContentTypesFilter(content_types=["photo", "document"]))

dp.message.register(cmd2_checking, CheckWords.checking)
                         
# --------------- START ---------------

async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
