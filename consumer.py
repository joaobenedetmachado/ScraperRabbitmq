import pika
import json
import pandas as pd
import os


data = []

def callback(ch, method, properties, body):
    global data
    noticia = json.loads(body)
    data.append(noticia)

    if len(data) % 5:
        salvar_excel()

def salvar_excel():
    df = pd.DataFrame(data)
    df.to_excel("noticias_recebidas.xlsx", index=False)
    print(" salva o excel ")

connRMQ = pika.BlockingConnection(pika.ConnectionParameters('localhost')) # just connect
channel = connRMQ.channel()

channel.queue_declare(queue='noticias')

channel.basic_consume(queue='noticias', on_message_callback=callback, auto_ack=True) # name of the queue, what function will be called

channel.start_consuming()