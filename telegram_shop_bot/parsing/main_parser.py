from .base_parser import *
from loader import db


class AsaxiyParser(BaseParser):
    def __init__(self, category):
        super(AsaxiyParser, self).__init__(category)

    def get_data(self):
        data = []
        soup = self.get_soup()
        box = soup.find('div', class_='row custom-gutter mb-40')
        products = box.find_all('div', class_='col-6 col-xl-3 col-md-4')
        category_name = ''
        if self.category == 'telefony-i-gadzhety/telefony':
            category_name = 'Telefonlar'
        elif self.category == 'kompyutery-i-orgtehnika/noutbuki':
            category_name = 'Noutbuklar'
        elif self.category == 'dlya-gejmerov':
            category_name = "Gamerler ushin"

        category_id = db.get_category_id(category_name)

        for prod in products:
            title = prod.find('p', class_='title__link').get_text(strip=True)
            price = int(
                prod.find('span', class_='product__item-price').get_text(strip=True).replace(' ', '').replace('сум',
                                                                                                              ''))
            image = prod.find('img', class_='img-fluid lazyload')['data-src']
            link = 'https://asaxiy.uz' + prod.find('a')['href']

            data.append({
                'product_name': title,
                'price': price,
                'image': image,
                'link': link,
                'category_id': category_id
            })
        return data
