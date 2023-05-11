import pika

# Установка соединения с RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создание очереди сообщений
channel.queue_declare(queue='messages')

# Отправка сообщения в очередь
message = 'Привет, бот!'
channel.basic_publish(exchange='', routing_key='messages', body=message)

# Закрытие соединения
connection.close()
