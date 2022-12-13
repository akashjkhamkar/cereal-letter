CREATE TABLE songs (
    id SERIAL PRIMARY KEY,
    Track VARCHAR NOT NULL,
    Album VARCHAR NOT NULL,
    Artists VARCHAR NOT NULL,
    Duration INTEGER NOT NULL
);

COPY songs(Track, Album, 
    Artists, Duration
) FROM '/tmp/songs.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM songs;
