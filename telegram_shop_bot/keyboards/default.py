from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton('Menu 🛍'), KeyboardButton('Korzinka 🛒'))
    markup.row(KeyboardButton('Baylanisiw 📞'), KeyboardButton('Sazlaw ⚙️'))
    return markup

def register_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('Dizimnen o\'tiw 📝'))
    return markup


def send_contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('Kontaktti jiberiw', request_contact=True))
    return markup

def categories_btns():
    categories = [item[0] for item in db.get_all_categories()]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for category in categories:
        markup.add(KeyboardButton(category))
    markup.add(KeyboardButton('Tiykarg\'i menu'))
    return markup


def admin_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton('Paydalaniwshilar sani'),
        KeyboardButton('Xabar jiberiw')

    )
    return markup



