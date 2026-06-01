import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    InlineKeyboardButton, 
    FSInputFile, 
    WebAppInfo, 
    MenuButtonWebApp
)
from aiogram.client.default import DefaultBotProperties 

# ==========================================
# КОНФИГУРАЦИЯ (Проект Eynec)
# ==========================================
TOKEN = "8752597276:AAEnYRqMQhaNXdvIge5pzQavv03otSnoOyc" 
ADMIN_USERNAME = "@Eynec" 
ADMIN_URL = "https://t.me/Eynec"
# ОБНОВЛЕННАЯ ССЫЛКА НА САЙТ
WEBSITE_URL = "https://eyneccheat3.github.io/Eynec/" 

# ТВОЙ ПОЛНЫЙ СПИСОК ФУНКЦИЙ
GAMES_DATA = {
    "bs": {
        "name": "🔫 Brawl Stars",
        "tariffs": {"1 Month": "250 Stars", "3 Months": "600 Stars", "Infinite": "1000 Stars"},
        "functions": (
            "⚙️ <b>Функции Brawl Stars</b>\n\n"
            "• 🎯 <b>Aimbot (Smart Focus)</b>: Авто-наведение с предиктами для 100% попадания.\n"
            "• 🛡️ <b>Auto-Dodge</b>: Анализ траекторий и автоматический увод от снарядов.\n"
            "• 🌿 <b>Bush ESP</b>: Подсветка контуров всех противников в кустах.\n"
            "• ⚡ <b>TP (Teleport Hack)</b>: Микро-перемещение для уклонения от ульты."
        )
    },
    "cr": {
        "name": "👑 Clash Royale",
        "tariffs": {"1 Month": "300 Stars", "3 Months": "600 Stars", "Infinite": "1000 Stars"},
        "functions": (
            "⚙️ <b>Функции Clash Royale</b>\n\n"
            "• 👁️ <b>Vision Core</b>: Отображение карт и эликсира врага в реальном времени.\n"
            "• 🌊 <b>Infinite Flow</b>: Обход лимитов для ускоренного накопления ресурсов.\n"
            "• 🤖 <b>AI Auto-Deployment</b>: Бот для контр-пиков и идеальных атак.\n"
            "• 🎨 <b>Visual Unlock</b>: Доступ ко всем скинам башен и эмодзи."
        )
    },
    "coc": {
        "name": "🏰 Clash of Clans",
        "tariffs": {"1 Month": "400 Stars", "3 Months": "800 Stars", "Infinite": "1500 Stars"},
        "functions": (
            "⚙️ <b>Функции Clash of Clans</b>\n\n"
            "• 🌾 <b>Auto-Farm & Loot Search</b>: Авто-поиск и сбор заданных ресурсов.\n"
            "• 🎮 <b>Attack Simulator (Sandbox)</b>: Тренировка атак без траты войск.\n"
            "• 💣 <b>Trap & Tesla Revealer</b>: Видимость всех скрытых ловушек и Тесл.\n"
            "• 📏 <b>Deployment Helper</b>: Отображение радиуса поражения защиты.\n"
            "• 🗺️ <b>Base Layout Importer</b>: Мгновенное копирование топовых баз.\n"
            "• 💂 <b>Auto-Train & Donation</b>: Авто-очередь войск и раздача доната."
        )
    }
}

# ==========================================
# ИНИЦИАЛИЗАЦИЯ
# ==========================================
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

class PromoState(StatesGroup):
    waiting_for_code = State()

# ==========================================
# КЛАВИАТУРЫ
# ==========================================
def get_main_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Купить", callback_data="catalog"))
    builder.row(InlineKeyboardButton(text="Поддержка", callback_data="support"))
    builder.row(InlineKeyboardButton(text="Активировать промокод", callback_data="promo"))
    builder.row(InlineKeyboardButton(text="Профиль", callback_data="profile"))
    return builder.as_markup()

def get_catalog_kb():
    builder = InlineKeyboardBuilder()
    for game_id, game_info in GAMES_DATA.items():
        builder.row(InlineKeyboardButton(text=game_info["name"], callback_data=f"game_{game_id}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="to_main"))
    return builder.as_markup()

def get_game_menu(game_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💰 Тарифы", callback_data=f"rates_{game_id}"))
    builder.row(InlineKeyboardButton(text="⚙️ Функции", callback_data=f"funcs_{game_id}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="catalog"))
    return builder.as_markup()

# ==========================================
# ЛОГИКА
# ==========================================

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    caption_text = (
        "👋 <b>Добро пожаловать в Eynec</b>\n\n"
        "<i>«Мы помогаем игрокам развиваться, а они помогают развиваться нам.»</i>\n\n"
        "Выберите нужный раздел:\n━━━━━━━━━━━━━━"
    )
    
    if os.path.exists("logo.jpg"):
        photo = FSInputFile("logo.jpg")
        await message.answer_photo(photo=photo, caption=caption_text, reply_markup=get_main_kb())
    else:
        await message.answer(caption_text, reply_markup=get_main_kb())

@dp.callback_query(F.data == "to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.answer("Выберите нужный раздел:\n━━━━━━━━━━━━━━", reply_markup=get_main_kb())
    await callback.answer()

@dp.callback_query(F.data == "catalog")
async def view_catalog(callback: types.CallbackQuery):
    await callback.message.answer("📚 <b>Каталог Eynec</b>\n\nВыберите игру:", reply_markup=get_catalog_kb())
    await callback.answer()

@dp.callback_query(F.data.startswith("game_"))
async def view_game(callback: types.CallbackQuery):
    game_id = callback.data.split("_")[1]
    game = GAMES_DATA[game_id]
    await callback.message.answer(f"{game['name']}\n\nВыберите раздел:", reply_markup=get_game_menu(game_id))
    await callback.answer()

@dp.callback_query(F.data.startswith("funcs_"))
async def view_funcs(callback: types.CallbackQuery):
    game_id = callback.data.split("_")[1]
    game = GAMES_DATA[game_id]
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"game_{game_id}"))
    await callback.message.answer(f"{game['functions']}\n━━━━━━━━━━━━━━", reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data.startswith("rates_"))
async def view_rates(callback: types.CallbackQuery):
    game_id = callback.data.split("_")[1]
    game = GAMES_DATA[game_id]
    text = f"{game['name']} — <b>Тарифы</b>\n\n"
    for name, price in game['tariffs'].items():
        text += f"• {name} — {price}\n"
    
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📨 Купить (Написать админу)", url=ADMIN_URL))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"game_{game_id}"))
    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data == "promo")
async def promo_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("🎁 <b>Введите промокод:</b>")
    await state.set_state(PromoState.waiting_for_code)
    await callback.answer()

@dp.message(PromoState.waiting_for_code)
async def promo_check(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="to_main"))
    await message.answer("❌ <b>Промокод неверный.</b>", reply_markup=builder.as_markup())
    await state.clear()

@dp.callback_query(F.data == "support")
async def support_view(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📨 Написать в поддержку", url=ADMIN_URL))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="to_main"))
    await callback.message.answer(f"🛠 <b>Поддержка Eynec</b>\n\nАдмин: {ADMIN_USERNAME}", reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data == "profile")
async def view_profile(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="to_main"))
    await callback.message.answer(f"👤 <b>Профиль</b>\n\nID: <code>{callback.from_user.id}</code>\nСтатус: Обычный", reply_markup=builder.as_markup())
    await callback.answer()

# ==========================================
# ЗАПУСК
# ==========================================
async def main():
    # Кнопка сайта "info" в углу ( Menu Button )
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="info", 
            web_app=WebAppInfo(url=WEBSITE_URL)
        )
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())