CREATE TABLE flux
(
    id    UUID,
    title TEXT,
    link  TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE article
(
    id          UUID,
    insertTime  TIMESTAMP,
    title       TEXT,
    link        TEXT,
    pubDate     TEXT,
    description TEXT,
    PRIMARY KEY (id,insertTime)
)
WITH CLUSTERING ORDER BY (insertTime desc);

CREATE TABLE user
(
    id              UUID,
    name TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE subscribe
(
    idFlux UUID,
    idUser UUID,
    PRIMARY KEY (idFlux, idUser)
);

CREATE TABLE articlebyuser
(
    iduser UUID,
    insertTime TIMESTAMP,
    idarticle UUID,
    idflux UUID,
    PRIMARY KEY (iduser,insertTime,idarticle)
)WITH CLUSTERING ORDER BY (insertTime desc);

CREATE TABLE articlebyflux
(
    idflux UUID,
    insertTime TIMESTAMP,
    idarticle UUID,
    PRIMARY KEY (idflux,insertTime,idarticle)
);