'''
    Author: Sydney Nguyen 
    cs257
    Database Assignment

'''

CREATE TABLE athletes (
        id INTEGER,
        athlete_name TEXT,
        athlete_sex TEXT,
    );

CREATE TABLE events (
        id INTEGER,
        event_name TEXT,
        sport_name TEXT
    );

CREATE TABLE games (
        id INTEGER,
        season TEXT,
        city TEXT,
        game_year INTEGER,
        game TEXT
    );

CREATE TABLE noc(
        id INTEGER,
        noc_abreviation TEXT,
        noc_region TEXT
    );


CREATE TABLE results (
        athlete_id INTEGER,
        noc_id INTEGER,
        event_id INTEGER,
        games_id INTEGER,
        medal TEXT
    );
