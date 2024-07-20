import psycopg2

from config import DB_USER, DB_HOST, DB_NAME, DB_PASSWORD


class DataBase:
    def __init__(self):
        self.database = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD
        )

    def manager(self, sql, *args, commit:bool=False,
                                  fetchone:bool=False,
                                  fetchall:bool=False):

        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    return db.commit()
                elif fetchone:
                    return cursor.fetchone()
                elif fetchall:
                    return cursor.fetchall()


    def create_users_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(70),
            birthdate DATE,
            contact VARCHAR(15) UNIQUE
            
        )'''

        self.manager(sql, commit=True)

    def save_user(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id) VALUES(%s)
        ON CONFLICT DO NOTHING'''
        self.manager(sql, (telegram_id,), commit=True)

    def check_user(self, telegram_id):
        sql = '''SELECT * FROM users WHERE telegram_id=%s'''
        return self.manager(sql, telegram_id, fetchone=True)

    def update_user_info(self, full_name, birthdate, contact, telegram_id):
        sql = '''UPDATE users SET full_name=%s, birthdate=%s, contact=%s WHERE telegram_id=%s'''
        self.manager(sql, full_name, birthdate, contact, telegram_id, commit=True)

    def create_table_categories(self):
        sql = '''CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            category_name VARCHAR(70) UNIQUE
        )'''
        self.manager(sql, commit=True)

    def insert_category_name(self, category_name):
        sql = '''INSERT INTO categories(category_name) VALUES (%s) ON CONFLICT DO NOTHING'''
        self.manager(sql, (category_name,), commit=True)
    def create_table_products(self):
        sql = '''CREATE TABLE IF NOT EXISTS products(
           product_id SERIAL PRIMARY KEY,
           product_name VARCHAR(255) UNIQUE,
           price INTEGER,
           image TEXT,
           link TEXT,
           category_id INTEGER REFERENCES categories(category_id)
            
        )'''
        self.manager(sql, commit=True)

    def insert_product(self, product_name, price, image, link, category_id):
        sql = '''INSERT INTO products(product_name, price, image, link, category_id)
        VALUES(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING'''
        self.manager(sql, product_name, price, image, link, category_id, commit=True)


    def get_category_id(self, category_name):
        sql = '''SELECT category_id FROM categories WHERE category_name=%s'''
        return self.manager(sql, category_name, fetchone=True)[0]


    def get_all_categories(self):
        sql = '''SELECT category_name FROM categories'''
        return self.manager(sql, fetchall=True)

    def get_category_by_id(self, category_id):
        sql = '''SELECT category_name FROM categories WHERE category_id=%s'''
        return self.manager(sql, category_id, fetchone=True)[0]

    # def products_by_category(self, category):
    #     sql = '''SELECT * FROM products
    #     WHERE category_id=(SELECT category_id FROM categories WHERE category_name=%s)'''
    #     return  self.manager(sql, category, fetchall=True)

    def get_count_products(self, category):
        sql = '''SELECT count(product_id) FROM products
        WHERE category_id=(SELECT category_id FROM categories WHERE category_name=%s)'''
        return self.manager(sql, category, fetchone=True)[0]

    def products_by_category_pagination(self, category, limit, offset):
        sql = '''SELECT * FROM products
        WHERE category_id=(SELECT category_id FROM categories WHERE category_name=%s)
        LIMIT %s
        OFFSET %s'''
        return self.manager(sql, category, limit, offset, fetchall=True)

    def product_info(self, product_id):
        sql = '''SELECT * FROM products WHERE product_id=%s'''
        return self.manager(sql, product_id, fetchone=True)

    def users_count(self):
        sql = '''SELECT count(telegram_id) FROM users'''
        return self.manager(sql, fetchone=True)[0]

    def users_ids(self):
        sql = '''SELECT telegram_id FROM users'''
        return self.manager(sql, fetchall=True)







