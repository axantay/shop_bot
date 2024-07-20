from keyboards.default import main_menu
from keyboards.inline import card_btns

def get_text_reply_markup(data: dict):
    text = "Korzinka:\n"
    total_price = 0
    for product_name, item in data['card'].items():
        product_price = item['price']
        quantity = item['quantity']
        price = quantity * int(product_price)
        total_price += price
        text += f"""\n{product_name}
Bahasi: {quantity} * {product_price} = {price}"""
    if total_price == 0:
        text = "Korzinka bos!"
        markup = main_menu()
    else:
        text += f"\n\nJa\'mi bahasi: {total_price}"
        markup = card_btns(data['card'])
    return {'text': text, 'total_price': total_price, 'markup': markup}