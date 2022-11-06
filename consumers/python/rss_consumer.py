
from kafka import KafkaConsumer, KafkaProducer
import pandas as pd
import os, json
import ast
from cassandra.cluster   import Cluster
import uuid
#from cassandrautils import saveWeatherreport



if __name__ == "__main__":
    print("Starting RSS Consumer")
    # get topic
    ARTICLE_SINK_TOPIC = os.environ.get("ARTICLE_SINK_TOPIC", "articlesink")
    USER_SINK_TOPIC = os.environ.get("USER_SINK_TOPIC", "userlistsink")
    TOPIC_NAME = os.environ.get("TOPIC_NAME","projetRSS")


    KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")
    CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST", "cassandradb")
    CASSANDRA_KEYSPACE = os.environ.get("CASSANDRA_KEYSPACE", "projetrss")

    print("Setting up Kafka consumer at {}".format(KAFKA_BROKER_URL))

    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=[KAFKA_BROKER_URL])
    # producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda x: x.encode('utf8'),
        api_version=(0, 10, 1)
    )

    cluster = Cluster(['cassandradb'],port=9042)
    session = cluster.connect(CASSANDRA_KEYSPACE)
    # use this encoder in order to insert tuples
    session.encoder.mapping[tuple] = session.encoder.cql_encode_tuple
    session.encoder.mapping[list] = session.encoder.cql_encode_list_collection

    # test add article

    # print("test for Article ...")
    # id_generate = str(uuid.uuid1())
    # id_flux = str(uuid.uuid1())
    # id_tuple = (id_flux,id_generate)
    # print("type "+type(id_tuple))
    # idarticle = [id_tuple]
    # title = "Google Inc"
    # link = "www.google.com"
    # description ="Une description super !!!!"
    # pubDate = pd.to_datetime("now",utc=True)
    # date = pd.to_datetime("now",utc=True)
    #
    # exemple ={"id": id_generate,"idFlux": id_flux ,"insertTime" : date.strftime('%Y-%m-%d %H:%M:%S'), "title" : title, "link" : link, "pubDate" : pubDate.strftime('%Y-%m-%d'), "description": description}
    # test = pd.DataFrame([exemple])
    # exemple = json.dumps(exemple)
    # producer.send(ARTICLE_SINK_TOPIC, value = exemple)
    # print("Test Article FINISH")
    # print("----")
    # print("Test add to user")
    #
    # exemple2 = {"iduser": "b92c0997-d91b-4005-baa0-4fc1e17082c5", "idarticle": idarticle}
    # test = pd.DataFrame([exemple2])
    # exemple2 = json.dumps(exemple2)
    # print(exemple2)
    # producer.send(USER_SINK_TOPIC, value = exemple2)
    # print("FINISH")

    print('Waiting for msg...')
    for msg in consumer:
        # print('got one!')
        msg = msg.value.decode('utf8')
        #jsonData=json.loads(msg)
        data = ast.literal_eval(msg)
        df = pd.DataFrame([data])

        print(data)
        print(df.loc[0])

        id_generate = str(uuid.uuid1())
        id_flux = str(uuid.UUID(df.loc[0].idflux))
        title = str(df.loc[0].title)
        link = df.loc[0].link
        description = str(df.loc[0].description)

        pubDate = df.loc[0].pubdate
        date = pd.to_datetime("now")

        dic = {"id": id_generate,"insertTime" : date.strftime('%Y-%m-%d %H:%M:%S'), "title" : title, "link" : link, "pubDate" : pubDate, "description": description}

        df = pd.DataFrame([dic])
        dic = json.dumps(dic)
        producer.send(ARTICLE_SINK_TOPIC, value = dic)

        #query get all user subscribe to the flux
        users_prepare = session.prepare("SELECT idUser FROM subscribe WHERE idFlux=?")
        users = session.execute(users_prepare, [uuid.UUID(id_flux)])

        idarticle = id_generate
        for user in users :
            print(user)
            #t = (id_flux,user)
            dic = {"idarticle":idarticle, "iduser": str(user.iduser),"idflux":id_flux, "inserttime":date.strftime('%Y-%m-%d %H:%M:%S')}
            #df = pd.DataFrame([dic])
            dic = json.dumps(dic)
            producer.send(USER_SINK_TOPIC, value = dic)
        
    print("Bye-Bye")