import os
import asyncio
import re

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand,
    FSInputFile,
)

# ====== TOKEN ======
BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in Render Environment Variables")

if not re.match(r"^\d+:[A-Za-z0-9_-]{20,}$", BOT_TOKEN):
    raise RuntimeError("BOT_TOKEN format is invalid")

print("BOT_TOKEN loaded successfully")

# ====== BOT ======
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

IMAGE_FILE = "image.jpg"

inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отзывы", url="https://t.me/+kO5zIxILayw0MjMy")],
    [InlineKeyboardButton(text="Тарифы", callback_data="msg1")],
    [InlineKeyboardButton(text="Купить", callback_data="msg2")],
    [InlineKeyboardButton(text="Часто задаваемые вопросы", callback_data="msg3")],
])

@dp.message(Command("start"))
async def start(message: types.Message):
    photo = FSInputFile(IMAGE_FILE)
    await message.answer_photo(photo, caption="Выберите опцию:", reply_markup=inline_kb)

@dp.callback_query(lambda c: c.data in {"msg1", "msg2", "msg3", "restart"})
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "restart":
        await callback.message.edit_text("Выберите опцию:", reply_markup=inline_kb)

    elif callback.data == "msg1":
        await callback.message.answer(
            "💰 Тарифы\n\n"
            "1 месяц — 1000₽\n"
            "6 месяцев — 5000₽\n"
            "12 месяцев — 10000₽\n"
            "Навсегда — 15000₽",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="restart")]]
            )
        )

    elif callback.data == "msg2":
        await callback.message.answer(
            "💳 Для покупки пиши 👉 @Neckfee",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="restart")]]
            )
        )

    elif callback.data == "msg3":
        await callback.message.edit_text(
            "💡 Часто задаваемые вопросы\n\n"
            "🎓 Формат: онлайн\n"
            "🚀 Первые клиенты: 3–6 недель\n"
            "⏰ Время: 1–2 часа в день\n"
            "💸 Доход: 50–150 тыс.+",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="restart")]]
            )
        )

    await callback.answer()

async def main():
    try:
        me = await bot.get_me()
        print(f"Authorized as @{me.username} ({me.id})")

        await bot.set_my_commands([
            BotCommand(command="start", description="Меню"),
            BotCommand(command="questions", description="Вопросы"),
            BotCommand(command="buy", description="Купить"),
            BotCommand(command="subscriptions", description="Тарифы"),
            BotCommand(command="reviews", description="Отзывы"),
        ])

        await dp.start_polling(bot)

    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())