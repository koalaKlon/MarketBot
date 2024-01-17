from typing import Union

from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message

from kb import main_menu, button_shop, unique_columns_list, handle_shop, menu, unique_shops, handle_category, \
    discount_info, handle_discount

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text="Рады вас видеть в MarketBot!", reply_markup=menu)
    await msg.answer(text="", reply_markup=await main_menu(msg))


@router.message()
async def keyboard_handler(msg: Union[Message, types.CallbackQuery]):
    if msg.text == "Категории":
        await main_menu(msg)
    elif msg.text == "Магазины":
        await button_shop(msg)


@router.callback_query()
async def button_handler(query: types.CallbackQuery):
    print(f"Called button_handler with data: {query.data}")
    data = query.data
    if data == 'button_магазины':
        print("Handling shops")
        await button_shop(query)
    elif data == 'menu':
        print("Handling menu")
        await main_menu(query.message)
    elif data in unique_shops:
        print(f"Handling shop: {data}")
        await handle_shop(query, data)
    elif data in unique_columns_list:
        print(f"Handling category: {data}")
        await handle_category(query, data)
    else:
        for shop in discount_info:
            if data in [info[1] for info in discount_info[shop]]:
                print(f"Handling discount: {data}")
                await handle_discount(query, shop, data)
                break




