#!/bin/sh

echo "Starting Article sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "articlesink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "articlesink",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.articlesink.projetrss.article.mapping": "id=value.id, inserttime=value.insertTime, description=value.description, title=value.title, link=value.link, pubdate=value.pubDate",
    "topic.articlesink.projetrss.article.consistencyLevel": "LOCAL_QUORUM"
  }
}'

echo "Starting UserList sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "userlistsink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "userlistsink",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.userlistsink.projetrss.articlebyuser.mapping": "idarticle=value.idarticle, iduser=value.iduser, inserttime=value.inserttime,idflux=value.idflux",
    "topic.userlistsink.projetrss.articlebyuser.consistencyLevel": "LOCAL_QUORUM"
  }
}'

echo "Done."
