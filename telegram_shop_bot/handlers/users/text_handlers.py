from telebot.types import Message, ReplyKeyboardRemove

from loader import bot, db
from keyboards.default import *
from keyboards.inline import products_pagination
from states import RegisterStates
from .utils import get_text_reply_markup


@bot.message_handler(func=lambda message: message.text =='Menu 🛍')
def reaction_menu(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    check = db.check_user(user_id)
    if None in check:
        bot.send_message(chat_id, "Buyirtpa beriw ushin iltimas, dizimnen otin\'😊", reply_markup=register_btn())
    else:
        bot.send_message(chat_id, 'Kategoriyani saylan\'', reply_markup=categories_btns())

# # # Register part # # #


@bot.message_handler(func=lambda message: message.text =='Dizimnen otiw 📝')
def reaction_register_btn(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_message(chat_id, 'Toliq F.I.O jazin\':', reply_markup=ReplyKeyboardRemove())
    bot.set_state(user_id, RegisterStates.full_name, chat_id)

@bot.message_handler(content_types=['text'], state=RegisterStates.full_name)
def reaction_full_name(message: Message):
   chat_id = message.chat.id
   user_id = message.from_user.id
   name = ''.join([name.capitalize() for name in message.text.split(' ')])
   with bot.retrieve_data(user_id, chat_id) as data:
       data['full_name'] = name
       data['telegram_id'] = user_id

   bot.send_message(chat_id, "Tuwilg\'an kunin\'izdi jazin\': jjjj.mm.dd")
   bot.set_state(user_id, RegisterStates.birthdate, chat_id)

@bot.message_handler(content_types=['text'], state=RegisterStates.birthdate)
def reaction_birthdate(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bd = message.text
    with bot.retrieve_data(user_id, chat_id) as data:
        data['birthdate'] = bd
    bot.send_message(chat_id, 'Nomerin\'izdi jazin\':', reply_markup=send_contact())
    bot.set_state(user_id, RegisterStates.contact, chat_id)


@bot.message_handler(content_types=['text', 'contact'], state=RegisterStates.contact)
def reaction_contact(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        if message.contact:
            data['contact'] = message.contact.phone_number
            db.update_user_info(**data)
            bot.delete_state(user_id, chat_id)
            bot.send_message(chat_id, 'Menu', reply_markup=main_menu())

        else:
            import re
            contact = message.text
            check = re.match(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', contact)
            if check:

                data['contact'] = message.text
                db.update_user_info(**data)
                bot.delete_state(user_id, chat_id)
                bot.send_message(chat_id, 'Menu', reply_markup=main_menu())

            else:
                bot.send_message(chat_id, 'Qatelik, qaytadan jazin\':', reply_markup=send_contact())
                bot.set_state(user_id, RegisterStates.contact, chat_id)


# # # End # # #

@bot.message_handler(content_types=['text'], func=lambda message: message.text == 'Tiykarg\'i menu')

def reaction_main_menu(message: Message):
    chat_id =message.chat.id
    bot.send_message(chat_id, 'Tiykarg\'i menu', reply_markup=main_menu())


@bot.message_handler(func=lambda message: message.text in [item[0] for item in db.get_all_categories()])
def reaction_to_category(message: Message):
    chat_id = message.chat.id
    category = message.text
    bot.send_message(chat_id, 'Ku\'tip turin\':', reply_markup=ReplyKeyboardRemove())
    bot.delete_message(chat_id, message.id + 1)
    bot.send_message(chat_id, "O\'nimler:", reply_markup=products_pagination(category))


@bot.message_handler(func=lambda message: message.text == 'Korzinka 🛒')
def reaction_basket(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        res = get_text_reply_markup(data)
    text = res['text']
    markup = res['markup']
    bot.send_message(chat_id, text, reply_markup=markup)




