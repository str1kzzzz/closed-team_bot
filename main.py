import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# Токен бота — вставляй напрямую, иначе PythonAnywhere не увидит переменную
BOT_TOKEN = "8498988807:AAEnH5BNh_Wc9xLW-HRcseQwgQZHtWjlTdo"

# Путь к файлу картинки
IMAGE_FILE = "image.jpg"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню
inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отзывы", url="https://t.me/+kO5zIxILayw0MjMy")],
    [InlineKeyboardButton(text="Тарифы", callback_data="msg1")],
    [InlineKeyboardButton(text="Купить", callback_data="msg2")],
    [InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data="msg3")],
])


# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer_photo(IMAGE_FILE, caption="Выберите опцию:", reply_markup=inline_kb)


# Обработка нажатий кнопок
@dp.callback_query(lambda c: c.data in ["msg1", "msg2", "msg3", "restart"])
async def process_callback(callback: types.CallbackQuery):

    if callback.data == "restart":
        await callback.message.edit_text("Выберите опцию:", reply_markup=inline_kb)

    elif callback.data == "msg1":
        text = (
            "💰 Тарифы на обучение\n\n"
            "1 месяц — 1000₽\n"
            "6 месяцев — 5000₽\n"
            "12 месяцев — 10000₽\n"
            "Навсегда — 15000₽"
        )
        kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="restart")]]
        )
        await callback.message.answer(text, reply_markup=kb)

    elif callback.data == "msg2":
        text = (
            "💳 Готов начать обучение?\n\n"
            "Для покупки и подключения пиши:\n👉 @Neckfee"
        )
        kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="restart")]]
        )
        await callback.message.answer(text, reply_markup=kb)

    elif callback.data == "msg3":
        text = (
            "💡 Часто задаваемые вопросы\n\n"
            "🎓 Как будет проходить обучение?\n"
            "Онлайн-формат — видеоуроки, задания, чат поддержки.\n\n"
            "🚀 Когда возьму первого клиента?\n"
            "Обычно через 3–6 недель.\n\n"
            "⏰ Сколько времени уделять?\n"
            "Рекомендуем 1–2 часа в день.\n\n"
            "🧩 Что если не понимаю материал?\n"
            "Пиши в чат — помогут кураторы.\n\n"
            "💸 Сколько зарабатывают выпускники?\n"
            "От 50 000 до 100 000₽ в месяц, при активной работе — 150 000₽+."
        )
        kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="restart")]]
        )
        await callback.message.edit_text(text, reply_markup=kb)

    await callback.answer()


# Команда /questions
@dp.message(Command("questions"))
async def questions(message: types.Message):
    text = (
        "💡 Часто задаваемые вопросы…\n\n"
        "🎓 Как будет проходить обучение?\n"
        "Онлайн — уроки, задания, чат.\n\n"
        "🚀 Первые клиенты? Через 3–6 недель.\n\n"
        "⏰ Время? 1–2 часа в день.\n\n"
        "💸 Доход? 50–100 тыс., иногда 150 тыс.+"
    )
    await message.answer(text)


# Команда /buy
@dp.message(Command("buy"))
async def buy(message: types.Message):
    text = "💳 Для покупки — пиши 👉 @Neckfee"
    await message.answer(text)


# Команда /subscriptions
@dp.message(Command("subscriptions"))
async def subscriptions(message: types.Message):
    text = (
        "💰 Тарифы на обучение\n\n"
        "1 месяц — 1000₽\n"
        "6 месяцев — 5000₽\n"
        "12 месяцев — 10000₽\n"
        "Навсегда — 15000₽"
    )
    await message.answer(text)


# Команда /reviews
@dp.message(Command("reviews"))
async def reviews(message: types.Message):
    await message.answer("Отзывы: https://t.me/+kO5zIxILayw0MjMy")


# MAIN
async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Меню"),
        BotCommand(command="questions", description="Вопросы"),
        BotCommand(command="buy", description="Купить"),
        BotCommand(command="subscriptions", description="Тарифы"),
        BotCommand(command="reviews", description="Отзывы"),
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())