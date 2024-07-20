from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import db

# def products_btns(product_list):
#     markup = InlineKeyboardMarkup()
#     for product in product_list:
#         markup.add(InlineKeyboardButton(product[1], callback_data=f'product|{product[0]}'))
#
#     return markup


def products_pagination(category, page=1):
    markup = InlineKeyboardMarkup()
    limit = 5
    product_count = db.get_count_products(category)
    max_page = product_count // limit if product_count % limit == 0 else product_count // limit + 1
    offset = (page - 1) * limit
    products = db.products_by_category_pagination(category, limit, offset)
    for product in products:
        markup.add(InlineKeyboardButton(product[1], callback_data=f'product|{product[0]}'))


    preview_btn = InlineKeyboardButton('⬅️ ', callback_data='preview')
    page_btn = InlineKeyboardButton(page, callback_data=f'page|{category}')
    next_btn = InlineKeyboardButton('➡️ ', callback_data='next')


    if page == 1:
        markup.row(page_btn, next_btn)
    elif 1 < page < max_page:
        markup.row(preview_btn, page_btn, next_btn)
    elif page == max_page:
        markup.row(preview_btn, page_btn)

    markup.add(InlineKeyboardButton('Artqa qaytiw ⬅️', callback_data='back_categories'),
               InlineKeyboardButton('Tiykarg\'i menu', callback_data='main_menu'))
    return markup

def product_items(category_id, product_id, page, quantity=1):
    items = [
        InlineKeyboardButton('➖', callback_data='minus'),
        InlineKeyboardButton(quantity, callback_data=f'quantity|{page}'),
        InlineKeyboardButton('➕', callback_data='plus')
    ]
    add_card = InlineKeyboardButton('Korzinkag\'a qosiw', callback_data=f'add_card|{product_id}')
    card = InlineKeyboardButton('Korzinka', callback_data='show_card')
    back = InlineKeyboardButton('Artqa 🔙', callback_data=f'back_cat_id|{category_id}')
    main_menu = InlineKeyboardButton('Tiykarg\'i menu', callback_data='main_menu')
    return InlineKeyboardMarkup(keyboard=[
        items,
        [add_card, card],
        [back, main_menu]
    ])

def card_btns(data: dict):
    markup = InlineKeyboardMarkup(row_width=1)
    for product_name, items in data.items():
        product_id = items['product_id']
        btn = InlineKeyboardButton(f"❌ {product_name}", callback_data=f'remove|{product_id}')
        markup.add(btn)

    back = InlineKeyboardButton('Kategoriya', callback_data='back_categories')
    clear = InlineKeyboardButton('Tazalaw 🚮', callback_data='clear_card')
    submit = InlineKeyboardButton('Tastiyiqlaw ✅', callback_data='submit')
    markup.row(clear, submit)
    markup.row(back)
    return markup



