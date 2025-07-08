import requests
from bs4 import BeautifulSoup
import pika
import json

url = "https://g1.globo.com/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

posts = soup.find_all("div", class_="feed-post-body")

connRMQ = pika.BlockingConnection(pika.ConnectionParameters('localhost')) # connecting on the rabbitmq

channel = connRMQ.channel()

channel.queue_declare(queue='noticias') # now i am creating the queue called "noticias"

for post in posts:
    link_tag = post.find("a")
    if link_tag:
        title = link_tag.text.strip()
        link = link_tag['href']

        try:
            article_resp = requests.get(link, headers=headers)
            article_soup = BeautifulSoup(article_resp.text, 'html.parser')
            subtitle_tag = article_soup.find("h2", class_="content-head__subtitle")
            subtitle = subtitle_tag.text.strip() if subtitle_tag else ""
        except:
            subtitle = ""

        noticia = { # create de structure of the new's
            "title": title,
            "link": link,
            "subtitle": subtitle
        }

        channel.basic_publish( # and publish it for the consumer
            exchange='',
            routing_key='noticias',
            body=json.dumps(noticia)
        )
        print(f"enviado: {title}")