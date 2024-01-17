import os
import gspread
import hashlib

from typing import Union
from dotenv import load_dotenv
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv()

gc = gspread.service_account(filename=os.getenv("FILENAME"))
worksheet = gc.open_by_key(os.getenv("GSHEET_KEY")).get_worksheet(0)

columns_list = worksheet.col_values(9)[1:]
unique_columns_list = list(set(columns_list))

shops_list = worksheet.col_values(1)[1:]
unique_shops = list(set(shops_list))


async def main_menu(msg):
    builder = InlineKeyboardBuilder()
    builder.button(text="Список магазинов", callback_data=f"button_магазины")
    for i in unique_columns_list:
        builder.button(text=f"{i}", callback_data=f"{i}")
    builder.button(text="Таблица со всеми Промокодами!",
                   url="https://docs.google.com/spreadsheets/d/1FhYGE5IODqbtXSfQGBs0BGUaUJYAWBGAC2SRWqYzf6M/edit#gid=0")
    builder.adjust(1)
    try:
        await msg.edit_text("Выберите категорию в которой хотите получить скидку⬇️", reply_markup=builder.as_markup())
    except:
        await msg.answer("Выберите категорию в которой хотите получить скидку⬇️", reply_markup=builder.as_markup())


async def button_shop(query: Union[Message, types.CallbackQuery]):
    try:
        builder = InlineKeyboardBuilder()
        for shop in unique_shops:
            callback_data = f"{shop}"
            if len(callback_data.encode('utf-8')) <= 64:
                builder.button(text=f"{shop}", callback_data=callback_data)
            else:
                short_shop_name = shop[:10]
                unique_id = generate_unique_id(shop)
                callback_data = f"{short_shop_name}_{unique_id}"
                builder.button(text=f"{shop}", callback_data=callback_data)
        builder.adjust(3)
        builder.button(text="В меню", callback_data="menu")
        await query.message.edit_text("Выбирайте🥰", reply_markup=builder.as_markup())
    except:
        await query.answer("Выбирайте🥰", reply_markup=builder.as_markup())


async def handle_shop(query: types.CallbackQuery, shop_name):
    builder = InlineKeyboardBuilder()
    for discount in shop_to_discounts[shop_name]:
        callback_data = f"{discount}"
        if len(callback_data.encode('utf-8')) <= 64:
            builder.button(text=f"{discount}", callback_data=callback_data)
        else:
            short_discount_name = discount[:10]
            unique_id = generate_unique_id(discount)
            callback_data = f"{short_discount_name}_{unique_id}"
            builder.button(text=f"{discount}", callback_data=callback_data)
    builder.button(text="В меню", callback_data="menu")
    builder.adjust(1)
    try:
        await query.message.edit_text(text=f"Выбирaйте🥰", reply_markup=builder.as_markup())
    except Exception as e:
        builder = InlineKeyboardBuilder()
        builder.button(text="В меню", callback_data="menu")
        builder.button(text="Подпишитесь на канал!", url="https://t.me/skidkinezagorami")
        builder.adjust(1)
        print(f"Exception occurred: {e}")
        await query.message.answer(text="Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте еще раз.",
                                   reply_markup=builder.as_markup())


async def handle_category(query: types.CallbackQuery, category):
    builder = InlineKeyboardBuilder()
    for shop in category_to_shops[category]:
        builder.button(text=f"{shop}", callback_data=f"{shop}")
    builder.button(text="В меню", callback_data="menu")
    builder.adjust(1)
    await query.message.edit_text(f"Выбирайте🥰", reply_markup=builder.as_markup())


async def handle_discount(query: types.CallbackQuery, shop_name, discount):
    builder = InlineKeyboardBuilder()
    for info in discount_info[shop_name]:
        if info[1] == discount:
            promo, discount, link, valid_until, region, conditions = info
            break
    builder.button(text="В меню", callback_data="menu")
    builder.button(text="Подпишитесь на канал!", url="https://t.me/skidkinezagorami")
    builder.adjust(1)
    await query.message.answer(f"Чтобы воспользоваться акцией необходимо: {conditions}")
    await query.message.answer(f"Название: {shop_name}\nСкидка: {discount}\nСсылка: {link}\nДействует до: {valid_until}\nРегион: {region}\nУсловия: {conditions}\nПромокод: {promo}")
    await query.message.answer("Куда отправимся за скидками дальше?", reply_markup=builder.as_markup())


def generate_unique_id(shop):
    return hashlib.md5(shop.encode()).hexdigest()[:8]


category_button = KeyboardButton(text='Категории')
market_button = KeyboardButton(text='Магазины')
menu = ReplyKeyboardMarkup(keyboard=[[category_button, market_button]], resize_keyboard=True)


discount_info = {}
for row in worksheet.get_all_values()[1:]:
    shop, promo, discount, link, valid_until, region, conditions = row[0], row[2], row[3], row[4], row[5], row[6], row[7]
    if shop not in discount_info:
        discount_info[shop] = []
    discount_info[shop].append((promo, discount, link, valid_until, region, conditions))


category_to_shops = {}
for category, shop in zip(worksheet.col_values(9)[1:], worksheet.col_values(1)[1:]):
    if category not in category_to_shops:
        category_to_shops[category] = []
    if shop not in category_to_shops[category]:
        category_to_shops[category].append(shop)


shop_to_discounts = {}
for shop, discount in zip(worksheet.col_values(1)[1:], worksheet.col_values(4)[1:]):
    if shop not in shop_to_discounts:
        shop_to_discounts[shop] = []
    if discount not in shop_to_discounts[shop]:
        shop_to_discounts[shop].append(discount)






