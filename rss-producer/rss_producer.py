import json
import os
from kafka import KafkaProducer
import uuid
import feedparser
from datetime import datetime
import time

def parseRSS(rss_url):
    parsed_feed = feedparser.parse(rss_url)
    return parsed_feed

def checkRSSDuplicate(feed,lastInsertLink):
    numberArticle = 0
    if(len(feed.entries)<=0):
        return numberArticle,lastInsertLink
    articleFirstLink = feed.entries[0].link
    for i in range(0,len(feed.entries)-1):
        articleLink= feed.entries[0].link
        if(lastInsertLink==articleLink):
            return numberArticle,articleFirstLink
        numberArticle+=1
    return numberArticle,articleFirstLink

def createArticle(entry,idflux):
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
    #print(summary)
    article = {
        'idflux': idflux,
        'title': title,
        'pubdate':published,
        'description': summary,
        'link':link,
    }
    return article
# Kafka settings
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL") if os.environ.get(
    "KAFKA_BROKER_URL") else 'localhost:9092'
TOPIC_NAME = os.environ.get("TOPIC_NAME") if os.environ.get("TOPIC_NAME") else 'projetRSS'

print("START")
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,value_serializer=lambda x: json.dumps(x).encode('utf8'),api_version=(0, 10, 1))

idflux = str(uuid.UUID('b92c0874-d91b-4005-baa0-4fc1e17082c5'))
url = "https://www.lemonde.fr/rss/une.xml"
lastArticleLink=""

while(True):
    feed = parseRSS(url)
    size,lastArticleLink=(checkRSSDuplicate(feed,lastArticleLink))

    for i in range(size):
        article = createArticle(feed.entries[i],idflux)
        producer.send(TOPIC_NAME, value=article)
        producer.flush()
    time.sleep(10)
    print(lastArticleLink)
    print("##############################--REFRESH--#######################################")
# for entry in feed.entries:
#     # Titre
#     title = entry.title
#     print(title)
#     # Date de publication
#     published = entry.published
#     print(published)
#     # Permalink
#     link = entry.link
#     print(link)
#     # Description sommaire
#     summary = entry.summary
#     print(summary)
#
#     article = {
#         'idflux': idflux,
#         'title': title,
#         'pubdate':published,
#         'description': summary,
#         'link':link,
#     }
#     producer.send(TOPIC_NAME, value=article)
#     producer.flush()
#     print("lunch to kafka !!")