from telebot.types import CallbackQuery

from loader import bot, db

from keyboards.default import *
from keyboards.inline import *
from states import *
from .utils import get_text_reply_markup
from shipping_data.shipping_detail import generated_product_invoice


@bot.callback_query_handler(func=lambda call: call.data == 'next')
def reaction_to_next(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards = call.message.reply_markup.keyboard[-2]
    for key in keyboards:
        if 'page' in key.callback_data:
            category = key.callback_data.split('|')[1]
            page = int(key.text)
            page += 1
            bot.edit_message_reply_markup(chat_id, call.message.id, reply_markup=products_pagination(category, page))






@bot.callback_query_handler(func=lambda call: call.data == 'preview')
def reaction_to_preview(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards = call.message.reply_markup.keyboard[-2]
    for key in keyboards:
        if 'page' in key.callback_data:
            category = key.callback_data.split('|')[1]
            page = int(key.text)
            page -= 1
            bot.edit_message_reply_markup(chat_id, call.message.id,
                                          reply_markup=products_pagination(category, page))


@bot.callback_query_handler(func=lambda call: call.data == 'back_categories')
def reaction_back_categories(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, "Kategoriyalar:", reply_markup=categories_btns())


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def reaction_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, 'Tiykarg\' menu', reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: 'page' == call.data.split('|')[0])
def reaction_page(call: CallbackQuery):
    keys = call.message.reply_markup.keyboard[-2]
    for key in keys:
        if 'page' in key.callback_data:
            page = key.text
            bot.answer_callback_query(call.id, f"Siz {page}shi bette turipsiz!")

@bot.callback_query_handler(func=lambda call: 'product' in call.data)
def reaction_product(call: CallbackQuery):
    product_id = call.data.split('|')[1]
    chat_id = call.message.chat.id
    keys = call.message.reply_markup.keyboard[-2]
    page = 1
    for key in keys:
        if 'page' in key.callback_data:
            page = key.text
    product_info = db.product_info(product_id)
    product_name = product_info[1]
    price = product_info[2]
    image = product_info[3]
    link = product_info[4]
    category_id = product_info[5]
    bot.delete_message(chat_id, call.message.id)
    # bot.send_message(chat_id, f"""O\'nim ati: <b>"{product_name}"</b>
    # Bahasi: <strong>{price}</strong> swm
    # <a href="{link}">Toliq mag'liwmat</a>
    # """, {image} parse_mode ='HTML')
    bot.send_photo(chat_id, image, caption=f"""O\'nim ati: <b>"{product_name}"</b>
Bahasi: <strong>{price}</strong> swm
<a href="{link}">Toliq mag'liwmat</a>
""", parse_mode='html', reply_markup=product_items(category_id, product_id, page))

@bot.callback_query_handler(func=lambda call: call.data in ['plus', 'minus'])
def reaction_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    category_id = call.message.reply_markup.keyboard[-1][0].callback_data.split("|")[1]
    page = call.message.reply_markup.keyboard[0][1].callback_data.split('|')[1]
    product_id = call.message.reply_markup.keyboard[1][0].callback_data.split("|")[1]
    if 'plus' in call.data:
        quantity += 1
        bot.edit_message_reply_markup(chat_id, call.message.id,
                reply_markup=product_items(category_id, product_id, page, quantity))

    else:
        if quantity > 1:
            quantity -= 1
            bot.edit_message_reply_markup(chat_id, call.message.id,
                      reply_markup=product_items(category_id, product_id, page, quantity))

        else:
            bot.answer_callback_query(call.id, 'Keminde 1 o\'nim boliwi sha\'rt!', show_alert=True)


@bot.callback_query_handler(func=lambda call: 'back_cat_id' in call.data)
def reaction_back_cat_id(call: CallbackQuery):
    chat_id = call.message.chat.id
    page = int(call.message.reply_markup.keyboard[0][1].callback_data.split('|')[1])
    category_id = int(call.data.split("|")[1])
    category = db.get_category_by_id(category_id)
    markup = products_pagination(category, page)
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, category, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: 'add_card' in call.data)
def reaction_add_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.answer_callback_query(call.id, 'Qosildi!')
    bot.set_state(user_id, CardStates.card, chat_id)
    product_id = int(call.data.split('|')[1])
    product = db.product_info(product_id)
    product_name = product[1]
    price = product[2]
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    with bot.retrieve_data(user_id, chat_id) as data:
        if data.get('card'):
            data['card'][product_name]= {
                    'product_id': product_id,
                    'price': price,
                    'quantity': quantity
            }
        else:
            data['card'] = {
                product_name: {
                    'product_id': product_id,
                    'price': price,
                    'quantity': quantity
                }
            }


@bot.callback_query_handler(func=lambda call: call.data == 'show_card')
def reaction_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.id)
    with bot.retrieve_data(user_id, chat_id) as data:
        res = get_text_reply_markup(data)
    text = res['text']
    markup = res['markup']
    bot.send_message(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: "remove" in call.data)
def reaction_remove(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    product_id = int(call.data.split('|')[1])
    with bot.retrieve_data(user_id, chat_id) as data:
        keys = [product_name for product_name in data['card'].keys()]
        for item in keys:
            if data['card'][item]['product_id'] == product_id:
                del data['card'][item]
    res =get_text_reply_markup(data)
    text = res['text']
    markup = res['markup']
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, text, reply_markup=markup)




@bot.callback_query_handler(func=lambda call: call.data == 'clear_card')
def reaction_clear_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.delete_state(user_id, chat_id)
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, 'Korzinka bosadi!', reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'submit')
def reaction_submit(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        bot.send_invoice(chat_id, **generated_product_invoice(data['card']).generated_invoice(), invoice_payload='shop_bot')











