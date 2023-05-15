import pika

# Функция для обработки полученного сообщения
def process_message(ch, method, properties, body):
    # Обработка полученного сообщения
    # ...

    # Отправка сообщения в очередь обработки
    channel.basic_publish(exchange='', routing_key='processing_queue', body=processed_message)

# Настройка соединения с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создание очереди для приема сообщений
channel.queue_declare(queue='incoming_queue')

# Указываем, какую функцию использовать для обработки сообщений
channel.basic_consume(queue='incoming_queue', on_message_callback=process_message, auto_ack=True)

# Запуск обработки сообщений
channel.start_consuming()
