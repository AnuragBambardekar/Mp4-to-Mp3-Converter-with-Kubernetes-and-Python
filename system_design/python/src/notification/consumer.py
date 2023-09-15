import pika, sys, os, time
from send import send_email

def main():
    #rabbitmq connection config
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq") # our service name is rabbitmq
    )
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = send_email.notification(body)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag) # acknowledge and remove message from queue

    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"),
        on_message_callback=callback
    )

    print("Waiting for messages. To Exit, Press CTRL+C")

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)