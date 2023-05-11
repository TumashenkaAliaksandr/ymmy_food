import pika
from rivescript import RiveScript

# Инициализация RiveScript
bot = RiveScript()

# Загрузка файлов с правилами бота
bot.load_directory('rive_directory')

# Подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создание очереди сообщений
channel.queue_declare(queue='messages')

# Обработка полученных сообщений
def process_message(ch, method, properties, body):
    message = body.decode('utf-8')

    # Ответ бота с использованием RiveScript
    response = bot.reply('user', message)

    # Вывод ответа бота
    print(f'Бот: {response}')

# Подписка на очередь и ожидание сообщений
channel.basic_consume(queue='messages', on_message_callback=process_message, auto_ack=True)
channel.start_consuming()
