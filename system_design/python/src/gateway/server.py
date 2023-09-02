import os, gridfs, pika, json # gridfs to store large files
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

# use RabbitMQ to store messages

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:271017//videos"

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()