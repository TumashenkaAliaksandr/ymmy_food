import pika

# Функция для обработки полученного сообщения
def process_message(ch, method, properties, body):
    # Обработка полученного сообщения
    pass

# Настройка соединения с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создание очереди для отправки сообщений
channel.queue_declare(queue='outgoing_queue')

# Указываем, какую функцию использовать для обработки сообщений
channel.basic_consume(queue='outgoing_queue', on_message_callback=process_message, auto_ack=True)

# Запуск обработки сообщений
channel.start_consuming()
