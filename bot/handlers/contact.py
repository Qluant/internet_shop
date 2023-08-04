from bot import bot, dp
from aiogram import types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IsSenderContact
from aiogram.dispatcher.filters.state import State, StatesGroup

from db.processing import get_user_data, add_phone_number, count_basket, is_banned

from ..processing.buttons import state_buttons, get_menu


states_sessions = dict()

class ContactForm(StatesGroup):
    phone_number = State()


state_button_text = "Скасувати додавання номеру"


@dp.message_handler(IsSenderContact(True), content_types=[types.ContentType.CONTACT])
async def instant_contact(message: types.Message):
    if is_banned(telegram_id=message.from_user.id):
        return None
    phone_number = message.contact.phone_number.strip('+')
    user = get_user_data(telegram_id=message.from_user.id)
    add_phone_number(user=user, phone_number=phone_number)
    admin_vision = True if user.role.title == "Admin" else False
    await message.reply(f"Ваш контакт ({phone_number}) було збережено! Тепер ви можете замовляти товари!", 
                        reply_markup=get_menu(admin_vision=admin_vision, contact_status=bool(user.phone_number), basket_emptiness=(count_basket(user=user)>0)))


@dp.message_handler(lambda message: message.text in ["Змінити номер телефону", "Додати номер телефону", "/contact", "/phone_number"] and not is_banned(telegram_id=message.from_user.id))
async def start_adding_contact(message: types.Message):
    states_sessions[message.from_user.id] = True
    await ContactForm.phone_number.set()
    await bot.send_message(chat_id=message.chat.id, text="Напишіть свій номер за зразком: \"380111111111\"", reply_markup=state_buttons("Скасувати"))


@dp.message_handler(lambda message: len(message.text) != 12 and not is_banned(telegram_id=message.from_user.id), state=ContactForm.phone_number)
async def invalid_length(message: types.Message, state: FSMContext):
    await message.reply("Невірна кількість цифр в номері телефона!", reply_markup=state_buttons(state_button_text))


@dp.message_handler(lambda message: not message.text.isdigit() and not is_banned(telegram_id=message.from_user.id), state=ContactForm.phone_number)
async def invalid_digit(message: types.Message, state: FSMContext):
    await message.reply("Невірна кількість цифр в номері телефона!", reply_markup=state_buttons(state_button_text))


@dp.message_handler(lambda message: len(message.text) == 12 and message.text.isdigit() and not is_banned(telegram_id=message.from_user.id), state=ContactForm.phone_number)
async def finish_adding_contact(message: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user = get_user_data(telegram_id=message.from_user.id)
    phone_number=message.text
    add_phone_number(user=user, phone_number=phone_number)
    admin_vision = True if user.role.title == "Admin" else False
    await message.reply(f"Ваш номер телефону ({phone_number}) було збережено! Тепер ви можете замовляти товари!", 
                        reply_markup=get_menu(admin_vision=admin_vision, contact_status=bool(user.phone_number), basket_emptiness=(count_basket(user=user)>0)))


@dp.callback_query_handler(lambda c: "stop" in c.data and not is_banned(telegram_id=c.message.from_user.id), state=ContactForm.phone_number)
async def state_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    states_sessions.pop(callback_query.from_user.id)
    await state.reset_state(with_data=False)
    await bot.send_message(chat_id=callback_query.message.chat.id, text="Скасувано покупки продукта")
