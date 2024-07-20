from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.types import BotCommand

from config import TOKEN
from database import DataBase



db = DataBase()


bot = TeleBot(TOKEN, state_storage=StateMemoryStorage(), use_class_middlewares=True)

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.ChatFilter())

bot.set_my_commands(
    commands=[
        BotCommand('start', 'Botti qayta iske tu\'siriw...')
    ]

)



