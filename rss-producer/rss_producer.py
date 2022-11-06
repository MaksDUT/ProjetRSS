import json
import os
from kafka import KafkaProducer
import uuid
import feedparser
from datetime import datetime


# Kafka settings
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL") if os.environ.get(
    "KAFKA_BROKER_URL") else 'localhost:9092'
TOPIC_NAME = os.environ.get("TOPIC_NAME") if os.environ.get("TOPIC_NAME") else 'projetRSS'


producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,value_serializer=lambda x: json.dumps(x).encode('utf8'),api_version=(0, 10, 1))

idflux = str(uuid.UUID('b92c0874-d91b-4005-baa0-4fc1e17082c5'))
url = "https://www.lemonde.fr/rss/une.xml"

feed = feedparser.parse(url)

for entry in feed.entries:
    # Titre
    title = entry.title
    print(title)
    # Date de publication
    published = entry.published
    print(published)
    # Permalink
    link = entry.link
    print(link)
    # Description sommaire
    summary = entry.summary
    print(summary)

    article = {
        'idflux': idflux,
        'title': title,
        'pubdate':published,
        'description': summary,
        'link':link,
    }
    producer.send(TOPIC_NAME, value=article)
    producer.flush()
    print("lunch to kafka !!")