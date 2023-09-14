import pika, json

# file, gridFS, rabbitmq channel, access
def upload(f, fs, channel, access):
    """
    - first upload the file to MongoDB using GridFS
    - put message on RabbitMQ queue
    - allowing us to form an asynchronous communication flow between gateway service
    and converter service.
    """
    try:
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return f"Internal Server Error!: {err}", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    # put the message on the queue
    """
    pika.spec.PERSISTENT_DELIVERY_MODE -->
    when messages are added to the queue, they need to be persisted
    so that if the pod is reset/crash/restart, the messages are still there.

    Make our queue Durable. Messages are not persisted forever. Only state is.
    """
    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        print(err)
        fs.delete(fid)
        return f"Internal Server Error!!: {err}", 500