from telebot.types import Message

from loader import bot, db
from config import ADMINS
from keyboards.default import admin_btn


@bot.message_handler(commands=['start'], chat_id=ADMINS)
def reaction_admins_commands(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Sa\'lem Admin", reply_markup=admin_btn())
