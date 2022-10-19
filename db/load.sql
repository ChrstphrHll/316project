\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV;
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_uid_seq',
                         (SELECT MAX(uid)+1 FROM Users),
                         false);


\COPY Games FROM 'Games.csv' WITH DELIMITER ',' NULL '' CSV;
SELECT pg_catalog.setval('public.games_gid_seq',
                         (SELECT MAX(gid)+1 FROM Games),
                         false);


\COPY LikesGame FROM 'LikesGame.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY ReviewOf FROM 'Reviews.csv' WITH DELIMITER ',' NULL '' CSV;
