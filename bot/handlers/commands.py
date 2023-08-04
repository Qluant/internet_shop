from bot import bot, dp
from aiogram import types

from db.processing import (
    get_user_data, get_users, is_registered, 
    is_banned, ban_user, unban_user,
    change_user_role, count_basket
    )

from ..processing.buttons import get_menu


@dp.message_handler(lambda message: message.text in ['/commands', 'Команди'])
async def admin_commands(message: types.Message):
    user = get_user_data(telegram_id=message.from_user.id)
    if user.role.title != 'Admin':
        await message.reply(text='У вас не вистачає прав на це.')
        return None
    await message.reply(text="Всі адмінські команди:\n\n/users - усі користувачі\n/ban <user_id> - блокування користувача\n/unban <user_id> - розблокувати користувача\n/promote <user_id> - зробити адміном\n/unpromote <user_id>- понизити адміна")


@dp.message_handler(lambda message: message.text in ['/users', 'Користувачі'])
async def command_users(message: types.Message):
    user = get_user_data(telegram_id=message.from_user.id)
    if user.role.title != 'Admin':
        await message.reply(text='У вас не вистачає прав на це.')
        return None
    text = "Користувачі:"
    for client in get_users():
        if not client.telegram_id is None:
            text += f'\n{client.moniker} - з id: ({client.telegram_id})'
    await message.reply(text=text)


@dp.message_handler(lambda message: message.text[:4] == '/ban')
async def command_ban(message: types.Message):
    user = get_user_data(telegram_id=message.from_user.id)
    if user.role.title != 'Admin':
        await message.reply(text='У вас не вистачає прав на це.')
        return None
    id = message.text[5:].strip()
    if id == '':
        await message.reply(f'Ви забули написати id користувача')
        return None
    if not id.isdigit():
        await message.reply(f'Id користувача повинно бути числом, а ні "{id}"')
        return None
    if is_registered(telegram_id=int(id)):
        banned = get_user_data(telegram_id=int(id))
        ban_user(telegram_id=int(id))
        await message.reply(f'Користувача з id "{id}" було заблоковано!')
        await bot.send_message(chat_id=banned.telegram_id, text="Вас було заблоковано!", reply_markup=None)
        return None
    await message.reply(f'Користувача з id "{id}" не існує, перевірте правильність написання id.')


@dp.message_handler(lambda message: message.text[:6] == '/unban')
async def command_unban(message: types.Message):
    user = get_user_data(telegram_id=message.from_user.id)
    if user.role.title != 'Admin':
        await message.reply(text='У вас не вистачає прав на це.')
        return None
    id = message.text[7:].strip()
    if id == '':
        await message.reply(f'Ви забули написати id користувача')
        return None
    if not id.isdigit():
        await message.reply(f'Id користувача повинно бути числом, а ні "{id}"')
        return None
    if is_registered(telegram_id=int(id)):
        if is_banned(telegram_id=id):
            unbanned = get_user_data(telegram_id=int(id))
            unban_user(telegram_id=int(id))
            await message.reply(f'Користувача з id "{id}" було разаблоковано!')
            await bot.send_message(chat_id=unbanned.telegram_id, text="Вас було разблоковано!", 
                                reply_markup=get_menu(admin_vision=False, contact_status=bool(unbanned.phone_number), basket_emptiness=(count_basket(user=unbanned)>0)))
            return None
        await message.reply(f'Користувача з id "{id}" і так не був заблокованим!')
    await message.reply(f'Користувача з id "{id}" не існує, перевірте правильність написання id.')


@dp.message_handler(lambda message: message.text[:8] == '/promote')
async def command_promote(message: types.Message):
    user = get_user_data(telegram_id=message.from_user.id)
    if user.role.title != 'Admin':
        await message.reply(text='У вас не вистачає прав на це.')
        return None
    id = message.text[9:].strip()
    if id == '':
        await message.reply(f'Ви забули написати id користувача')
        return None
    if not id.isdigit():
        await message.reply(f'Id користувача повинно бути числом, а ні "{id}"')
    if is_registered(telegram_id=int(id)):
        new_admin = get_user_data(telegram_id=int(id))
        change_user_role("Admin", user=new_admin)
        await message.reply(f'Користувача з id "{id}" було назначено адміном!')
        await bot.send_message(chat_id=new_admin.telegram_id, text="Вас було назначено адміном!", 
                            reply_markup=get_menu(admin_vision=True, contact_status=bool(new_admin.phone_number), basket_emptiness=(count_basket(user=new_admin)>0)))
        return None
    await message.reply(f'Користувача з id "{id}" не існує, перевірте правильність написання id.')


@dp.message_handler(lambda message: message.text[:10] == '/unpromote')
async def command_unpromote(message: types.Message):
    user = get_user_data(telegram_id=message.from_user.id)
    if user.role.title != 'Admin':
        await message.reply(text='У вас не вистачає прав на це.')
        return None
    id = message.text[11:].strip()
    if id == '':
        await message.reply(f'Ви забули написати id користувача')
        return None
    if not id.isdigit():
        await message.reply(f'Id користувача повинно бути числом, а ні "{id}"')
        return None
    if is_registered(telegram_id=int(id)):
        old_admin = get_user_data(telegram_id=int(id))
        if user.title.role == "Admin":
            change_user_role("Regular", user=old_admin)
            await message.reply(f'Користувача з id "{id}" більше не адмін!')
            await bot.send_message(chat_id=old_admin.telegram_id, text="Вас було прибрано з адмінів!", 
                                reply_markup=get_menu(admin_vision=True, contact_status=bool(old_admin.phone_number), basket_emptiness=(count_basket(user=old_admin)>0)))
            return None
        else:
            await message.reply(f'Користувача з id "{id}" і так не був адміном!')
            return None
    await message.reply(f'Користувача з id "{id}" не існує, перевірте правильність написання id.')
