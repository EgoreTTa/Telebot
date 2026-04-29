import telebot
import asyncio
import logging
import aiogram
import os

from dotenv import load_dotenv
from os import getenv
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import database as db

logging.basicConfig(level=logging.INFO)
load_dotenv()

API_TOKEN = getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("❌ Переменная API_TOKEN не найдена. Проверьте .env или окружение.")

bot = Bot(API_TOKEN)
dp = Dispatcher()
router = Router()

@dp.startup()
async def on_startup(bot: Bot):
    await db.init_db()
    logging.info("🗄 База данных инициализирована")

def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="👤 Мой профиль", callback_data="menu_profile")
    builder.button(text="⚙️ Настройки", callback_data="menu_settings")
    return builder.as_markup()

def get_settings_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Язык", callback_data="settings_language")
    builder.button(text="🔔 Уведомления", callback_data="settings_notifications")
    builder.button(text="🔙 Назад", callback_data="menu_back_to_main")
    return builder.as_markup()

def get_profile_view():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data="menu_back_to_main")
    return builder.as_markup()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await db.save_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    await message.answer(
        "Привет! Выберите действие:",
        reply_markup=get_main_menu()
    )

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    count = await db.get_total_users()
    await message.answer(f"📊 В базе данных зарегистрировано пользователей: `{count}`")

@router.callback_query(F.data.startswith("menu_"))
async def process_menu_callbacks(callback: CallbackQuery):
    if callback.data == "menu_profile":
        await callback.message.edit_text(
            "Это ваш профиль. Тут какая-то инфа из БД.",
            reply_markup=get_profile_view()
        )
    elif callback.data == "menu_settings":
        await callback.message.edit_text(
            "Раздел настроек:",
            reply_markup=get_settings_menu()
        )
    elif callback.data == "menu_back_to_main":
        await callback.message.edit_text(
            "Главное меню:",
            reply_markup=get_main_menu()
        )
    
    await callback.answer()

@router.callback_query(F.data.startswith("settings_"))
async def process_settings_callbacks(callback: CallbackQuery):
    if callback.data == "settings_language":
        await callback.message.edit_text(
            "Выберите язык (пример):",
        )
    elif callback.data == "settings_notifications":
        await callback.message.edit_text(
            "Управление уведомлениями...",
        )
    
    await callback.answer()

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
