# RSS Merger for Big-Data projet's university


# Quickstart instructions

#Create docker networks
```bash
$ docker network create kafka-network                         # create a new docker network for kafka cluster (zookeeper, broker, kafka-manager services, and kafka connect sink services)
$ docker network create cassandra-network                     # create a new docker network for cassandra. (kafka connect will exist on this network as well in addition to kafka-network)
```
## Starting Cassandra

Cassandra is setup so it runs keyspace, schema and insert data for the presentation. 

it's ready to use.
```bash
$ docker-compose -f cassandra/docker-compose.yml --env-file ./.env up -d 
```

## Starting kafka on docker
```bash
$ docker-compose  -f kafka/docker-compose.yml --env-file ./.env  up -d  # start single zookeeper, broker, kafka-manager and kafka-connect services
$ docker ps -a                                                # sanity check to make sure services are up: kafka_broker_1, kafka-manager, zookeeper, kafka-connect service
```

## Start consumer:
consumer get article from a producer from kafka pipline and create new object to insert into cassandra. 
```bash
$ docker-compose -f consumers/docker-compose.yml --env-file ./.env up -d        # start the consumers
```

## Starting Producers
the producer will get information from Lemonde RSS flux need to lunch every time for new article 
```bash
$ docker-compose -f rss-producer/docker-compose.yml --env-file ./.env  up -d # start the producer for rss
```

## Check all containers are running with
```bash
$ docker ps -a                                                # sanity check to make sure services are up: kafka_broker_1, kafka-manager, zookeeper, kafka-connect service
```
## Teardown

To stop all running kakfa cluster services

```bash
$ docker-compose -f consumers/docker-compose.yml down          # stop the consumer

$ docker-compose -f rss-producer/docker-compose.yml down       # stop rss producer

$ docker-compose -f kafka/docker-compose.yml down              # stop zookeeper, broker, kafka-manager and kafka-connect services

$ docker-compose -f cassandra/docker-compose.yml down          # stop Cassandra
```

To remove the kafka-network network:

```bash
$ docker network rm kafka-network
$ docker network rm cassandra-network
```