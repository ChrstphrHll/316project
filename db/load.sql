\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV;
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_uid_seq',
                         (SELECT MAX(uid)+1 FROM Users),
                         false);


\COPY Games FROM 'Games.csv' WITH DELIMITER '@' NULL '' CSV;
SELECT pg_catalog.setval('public.games_gid_seq',
                         (SELECT MAX(gid)+1 FROM Games),
                         false);


\COPY LikesGame FROM 'LikesGame.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Collections FROM 'Collections.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY CreatedBy FROM 'CreatedBy.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY HasGame FROM 'HasGame.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY ReviewOf FROM 'Reviews.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Mechanics FROM 'Mechanics.csv' WITH DELIMITER '@' NULL '' CSV;

\COPY Implements FROM 'Implements.csv' WITH DELIMITER '@' NULL '' CSV;

\COPY Copies FROM 'Copies.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY CopyOf FROM 'CopyOf.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Libraries FROM 'Libraries.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Owns FROM 'Owns.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY HasCopy FROM 'HasCopy.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY CheckedOutBy FROM 'CheckedOutBy.csv' WITH DELIMITER ',' NULL '' CSV;
