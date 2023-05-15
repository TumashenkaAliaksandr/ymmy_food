from peewee import *

# Создание подключения к базе данных SQLite
database = SqliteDatabase('inventory.db')

# Определение модели "Раздел"
class Category(Model):
    name = CharField()

    class Meta:
        database = database

# Определение модели "Товар"
class Product(Model):
    name = CharField()
    description = TextField()
    category = ForeignKeyField(Category, backref='products')

    class Meta:
        database = database

# Создание таблиц в базе данных
database.create_tables([Category, Product])
