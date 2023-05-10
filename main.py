import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import *
import json


# Инициализация бота
vk_session = vk_api.VkApi(token=YOUR_VK_API_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, YOUR_GROUP_ID)

# Словарь с информацией о разделах и товарах
catalog = {
    'Торты': [
        {'название': 'Торт 1', 'описание': 'Описание торта 1', 'фото': 'photo1.jpg'},
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
        product_index = int(message.split(':')[1].strip()) - 1
        send_product_info(user_id, product_index)

# Отправка главного меню
def send_main_menu(user_id):
    keyboard = {
        'one_time': False,
        'buttons': [
            [{'action': {'type': 'text', 'label': 'Торты'}, 'color': 'positive'},
             {'action': {'type': 'text', 'label': 'Пирожные'}, 'color': 'positive'},
             {'action': {'type': 'text', 'label': 'Кексы'}, 'color': 'positive'}]
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    vk.messages.send(user_id=user_id, message='Выберите раздел:', keyboard=keyboard, random_id=0)


# Отправка товаров выбранного раздела
def send_products(user_id, section):
    products = catalog[section]
    message = f'Раздел: {section}\n\n'
    for i, product in enumerate(products):
        message += f'{i+1}. {product["название"]}\n'
    message += '\nВведите номер товара для подробной информации:'
    vk.messages.send(user_id=user_id, message=message, random_id=0)

# Отправка информации о товаре
def send_product_info(user_id, section, product_index):
    product = catalog[section][product_index]
    message = f'Название: {product["название"]}\n'
    message += f'Описание: {product["описание"]}\n'
    message += f'Фото: {product["фото"]}\n'
    vk.messages.send(user_id=user_id, message=message, random_id=0)



def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            handle_new_message(event)

if __name__ == '__main__':
    main()