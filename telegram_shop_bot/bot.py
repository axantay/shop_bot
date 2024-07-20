from loader import bot, db
from parsing.main_parser import AsaxiyParser
from middlewares.antiflood import SimpleMiddleware

db.create_users_table()
db.create_table_categories()
db.create_table_products()
# categories = ['Telefonlar', 'Noutbuklar', 'Gamerler ushin']
# for category in categories:
#     db.insert_category_name(category)

# products = [AsaxiyParser('telefony-i-gadzhety/telefony').get_data(), AsaxiyParser('kompyutery-i-orgtehnika/noutbuki').get_data(), AsaxiyParser('dlya-gejmerov').get_data()]
#
# for item in products:
#     for product in item:
#         db.insert_product(**product)




import handlers


bot.setup_middleware(SimpleMiddleware(0.7))

if __name__=='__main__':
    print('Bot islep tur...\nhttps://t.me/intershopnet_bot')

    bot.infinity_polling()