import asyncio
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import logging
# Включаем логирование
logging.basicConfig(level=logging.INFO)
# Создаем объект бота
#API_TOKEN = os.getenv('TOKEN')
#API_TOKEN = os.getenv('token')
print(f"API_TOKEN: {API_TOKEN}")
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()
# Определяем кнопки
button1 = types.KeyboardButton(text="/start")
button2 = types.KeyboardButton(text="стоп")
button3 = types.KeyboardButton(text="инфо")
button4 = types.KeyboardButton(text="покажи лису")
button5 = types.KeyboardButton(text="закрыть")
# Создаем клавиатуру
keyboard1 = [
    [button2, button3, button4, button5],
    [button1]
]
kb1 = types.ReplyKeyboardMarkup(keyboard=keyboard1, resize_keyboard=True)
# Устанавливаем команды бота
async def set_commands():
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Начать общение"),
        types.BotCommand(command="стоп", description="Остановить бота"),
        types.BotCommand(command="инфо", description="Получить информацию"),
        types.BotCommand(command="покажи_лису", description="Показать лису"),  # Используйте underscore вместо пробела
        types.BotCommand(command="закрыть", description="Закрыть бота")
    ])
# Хэндлер на команду /start
@dp.message(Command("start"))
async def command_start(message: types.Message):
    await message.answer("Привет! Я эхобот на aiogram 3. Отправь мне сообщение, и я его повторю", reply_markup=kb1)


# Хэндлер для текстовых сообщений
@dp.message(lambda message: message.text is not None)  # Обработка всех текстовых сообщений
async def msg_echo(message: types.Message):
    msg_user = message.text.lower()
    name = message.chat.first_name
    if "привет" in msg_user:
        await message.answer(f"Привет-привет, {name}", reply_markup=kb1)


    elif "пока" == msg_user:
        await message.answer(f"Пока-пока, {name}", reply_markup=kb1)
    elif "ты кто" in msg_user:
        await message.answer(f"Я бот, {name}", reply_markup=kb1)
    elif "стоп" in msg_user:
        await message.answer(f"Ты меня не остановишь !!!", reply_markup=kb1)
    elif "инфо" in msg_user:
        await message.answer(f"Я Bot, меня зовут Ёжик  !", reply_markup=kb1)
    elif "покажи лису" in msg_user:
        await show_fox(message)
    elif "закрыть" in msg_user:
        await message.answer(f"Ха-Ха, ты меня не закроешь  !", reply_markup=kb1)
    else:
        await echo(message)

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)
# Хэндлер для команды /Покажи лису
@dp.message(Command("покажи_лису"))  # Используйте underscore для команд
async def show_fox(message: types.Message):
    fox_image_url = await get_fox_image()
    if fox_image_url:
        await message.answer_photo(fox_image_url, caption="Вот лиса для тебя!")
    else:
        await message.answer("Не удалось получить изображение лисы.")
# Функция для получения изображения лисы
async def get_fox_image():
    url = "https://randomfox.ca/floof/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("image")
            else:
                return None



# Основная функция для запуска бота
async def main():
    #await set_commands()  # Устанавливаем команды
    await dp.start_polling(bot)
# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
