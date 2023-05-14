import random
import requests
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from googletrans import Translator
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cb = CallbackData('keyboard', 'action')
ACCESS_KEY = 'J20YlJh8o_ZcCqCNCKFiSMz-m4XSHzefYR3TRgGNJOU'
bot = Bot(token='5852147840:AAGe4IOo8mGCJy5aaj-2duhos6FQx2iWtBY')
storage = MemoryStorage()
dp = Dispatcher(bot, storage)
k = 0


@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    global k
    keyboard = types.InlineKeyboardMarkup()
    photos_button = types.InlineKeyboardButton('Фотографии', callback_data=cb.new(action='photos'))
    text_button = types.InlineKeyboardButton('Текст', callback_data=cb.new(action='text'))
    styles_button = types.InlineKeyboardButton('Стили', callback_data=cb.new(action='styles'))
    keyboard.row(photos_button, text_button, styles_button)
    await message.reply('Выберите действие:', reply_markup=keyboard)
    k = 0


@dp.callback_query_handler(cb.filter(action='photos'))
async def handle_photos(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите категорию фотографий:')
    global k
    k = 1


@dp.callback_query_handler(cb.filter(action='text'))
async def handle_text(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите тему для поиска в Википедии:')
    global k
    k = 2


@dp.callback_query_handler(cb.filter(action='styles'))
async def handle_text(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    index = random.randint(0, 1614)
    await bot.send_message(callback_query.from_user.id, 'Вот сайт с бесплатными стилями для вашей презентации:')
    await bot.send_message(callback_query.from_user.id, f'https://www.powerpointbase.com/index.php?newsid={index}')
    await bot.send_message(callback_query.from_user.id, 'Чтобы получить другой стиль отправьте что угодно.')
    global k
    k = 3




@dp.message_handler()
async def handle_message(message: types.Message):
    global k
    if k == 1:
        category = message.text.replace('/photos', '').strip()
        translator = Translator()
        result = translator.translate(category, src='ru', dest='en')
        image_url = get_random_image(result.text)
        if image_url:
            await bot.send_photo(message.from_user.id, photo=image_url)
            await bot.send_message(message.from_user.id, text='Вы можете продолжать искать фотографии. Просто заново введите категорию.')
        else:
            await bot.send_message(message.from_user.id, 'Не удалось найти фотографии для указанной категории.')
    elif k == 2:
        txt = message.text.replace('/text', '').strip()
        txt_re = txt.split(' ')
        txt_re_re = '_'.join(txt_re)
        translator = Translator()
        result = translator.translate(txt, src='ru', dest='en')
        category = result.text
        txt_re_eng = category.split(' ')
        txt_re_re_eng = '_'.join(txt_re_eng)
        await bot.send_message(message.from_user.id, text=f'https://ru.wikipedia.org/wiki/{txt_re_re}')
        await bot.send_message(message.from_user.id, text=f'https://en.wikipedia.org/wiki/{txt_re_re_eng}')
        await bot.send_message(message.from_user.id, text='Вы можете продолжать искать текст. Просто введите новую тему.')
    elif k == 3:
        index = random.randint(0, 1614)
        await bot.send_message(message.from_user.id, f'https://www.powerpointbase.com/index.php?newsid={index}')
        await bot.send_message(message.from_user.id, text='Чтобы получить другой стиль отправьте что угодно.')
    else:
        await bot.send_message(message.from_user.id,
                               'Я вас не понял. Напишите /start, чтобы получить все доступные команды.')
    keyboard = types.InlineKeyboardMarkup()
    photos_button = types.InlineKeyboardButton('Фотографии', callback_data=cb.new(action='photos'))
    text_button = types.InlineKeyboardButton('Текст', callback_data=cb.new(action='text'))
    styles_button = types.InlineKeyboardButton('Стили', callback_data=cb.new(action='styles'))
    keyboard.row(photos_button, text_button, styles_button)
    await message.reply('Выберите действие:', reply_markup=keyboard)


def get_random_image(category):
    url = f"https://api.unsplash.com/photos/random?query={category}&client_id={ACCESS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'urls' in data and 'regular' in data['urls']:
            return data['urls']['regular']
    return None


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)