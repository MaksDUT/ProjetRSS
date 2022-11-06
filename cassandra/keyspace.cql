CREATE KEYSPACE IF NOT EXISTS projetrss
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };