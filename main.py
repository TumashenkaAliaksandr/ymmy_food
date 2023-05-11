import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from peewee import *
import json
from config import *


# Инициализация бота
vk_session = vk_api.VkApi(token=YOUR_VK_API_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, YOUR_GROUP_ID)

# Подключение к базе данных
db = SqliteDatabase('catalog.db')


# Модель для таблицы разделов
class Section(Model):
    name = CharField()

    class Meta:
        database = db


# Модель для таблицы товаров
class Product(Model):
    name = CharField()
    description = TextField()
    photo = CharField()
    section = ForeignKeyField(Section, backref='products')

    class Meta:
        database = db


# Создание таблиц в базе данных
db.create_tables([Section, Product])


def upload_photo(photo_url):
    upload_url = vk.photos.getMessagesUploadServer()['upload_url']
    response = requests.post(upload_url, files={'photo': requests.get(photo_url).content})
    result = json.loads(response.text)
    photo = vk.photos.saveMessagesPhoto(**result)[0]
    return f"photo{photo['owner_id']}_{photo['id']}"

# Заполнение базы данных из словаря catalog
def populate_database():
    with db.atomic():
        for section_name, products in catalog.items():
            section = Section.create(name=section_name)
            for product in products:
                photo_id = upload_photo(product['фото'])  # Загрузка фото и получение идентификатора
                Product.create(
                    name=product['название'],
                    description=product['описание'],
                    photo=photo_id,
                    section=section
                )



# Словарь с информацией о разделах и товарах
catalog = {
    'Торты': [
        {'название': 'Торт 1', 'описание': 'Описание торта 1', 'фото': 'images/celebration-birthday-cake.jpg'},
        {'название': 'Торт 2', 'описание': 'Описание торта 2', 'фото': 'photo2.jpg'}
    ],
    'Пирожные': [
        {'название': 'Пирожное 1', 'описание': 'Описание пирожного 1', 'фото': 'photo3.jpg'},
        {'название': 'Пирожное 2', 'описание': 'Описание пирожного 2', 'фото': 'photo4.jpg'}
    ],
    'Кексы': [
        {'название': 'Кекс 1', 'описание': 'Описание кекса 1', 'фото': 'photo5.jpg'},
        {'название': 'Кекс 2', 'описание': 'Описание кекса 2', 'фото': 'photo6.jpg'}
    ]
}

# Заполнение базы данных
populate_database()


# Обработчик новых сообщений
def handle_new_message(event):
    user_id = event.obj.message['from_id']
    message = event.obj.message['text']

    if message == 'Начать':
        send_main_menu(user_id)
    elif message == 'Назад':
        send_main_menu(user_id)
    elif message in catalog.keys():
        send_products(user_id, message)
    elif message.startswith('Товар:'):
        try:
            product_index = int(message.split(':')[1].strip()) - 1
            send_product_info(user_id, product_index)
        except (ValueError, IndexError):
            vk.messages.send(user_id=user_id, message='Некорректный номер товара.', random_id=0)


# Отправка главного меню
def send_main_menu(user_id):
    keyboard = {
        'one_time': False,
        'buttons': [
            [{'action': {'type': 'text', 'label': 'Торты'}, 'color': 'positive'},
             {'action': {'type': 'text', 'label': 'Пирожные'}, 'color': 'positive'},
             {'action': {'type': 'text', 'label': 'Кексы'}, 'color': 'positive'}],
            [{'action': {'type': 'text', 'label': 'Назад'}, 'color': 'negative'}]
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    vk.messages.send(user_id=user_id, message='Выберите раздел:', keyboard=keyboard, random_id=0)

# Отправка товаров выбранного раздела
def send_products(user_id, section):
    products = Product.select().join(Section).where(Section.name == section)
    message = f'Раздел: {section}\n\n'
    for i, product in enumerate(products):
        message += f'{i + 1}. {product.name}\n'
    message += '\nВведите номер товара для подробной информации:'
    vk.messages.send(user_id=user_id, message=message, random_id=0)

# Отправка информации о товаре
def send_product_info(user_id, product_index):
    product = Product.select().join(Section).where(Product.id == product_index).first()
    if product:
        message = f'Название: {product.name}\n'
        message += f'Описание: {product.description}\n'
        message += f'Фото: {product.photo}\n'
        vk.messages.send(user_id=user_id, message=message, random_id=0)

def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            handle_new_message(event)

if __name__ == '__main__':
    main()
