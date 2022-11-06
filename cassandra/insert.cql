-- insert user
INSERT INTO user (id, name) VALUES(b92c0997-d91b-4005-baa0-4fc1e17082c5 , 'maxime');
INSERT INTO user (id, name) VALUES(b92c0615-d91b-4005-baa0-4fc1e17082c5 , 'leane');
INSERT INTO user (id, name) VALUES(b92c5614-d91b-4005-baa0-4fc1e17082c5 , 'guillaume');
-- insert flux
INSERT INTO flux (id, link,title) VALUES(b92c0874-d91b-4005-baa0-4fc1e17082c5 , 'https://www.lemonde.fr/rss/une.xml','Le Monde.fr - Actualités et Infos en France et dans le monde');
INSERT INTO flux (id, link,title) VALUES(b92c0138-d91b-4005-baa0-4fc1e17082c5 , 'https://www.economie.gouv.fr/rss/toutesactualites','gouv Eco - Flux RSS Toutes les actualités');
-- insert subscribe
INSERT INTO subscribe (idflux,iduser) VALUES(b92c0874-d91b-4005-baa0-4fc1e17082c5 , b92c0997-d91b-4005-baa0-4fc1e17082c5);
INSERT INTO subscribe (idflux,iduser) VALUES(b92c0138-d91b-4005-baa0-4fc1e17082c5 , b92c0997-d91b-4005-baa0-4fc1e17082c5);
INSERT INTO subscribe (idflux,iduser) VALUES(b92c0138-d91b-4005-baa0-4fc1e17082c5 , b92c0615-d91b-4005-baa0-4fc1e17082c5);
