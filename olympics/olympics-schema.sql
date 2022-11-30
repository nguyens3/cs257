CREATE TABLE athletes (
    id SERIAL, 
    name text, 
    sex text);
    
CREATE TABLE NOC (
    id SERIAL, 
    abbreviation text, 
    region text);

CREATE TABLE olympic_games (
    id SERIAL, 
    year integer, 
    season text, 
    city text);

CREATE TABLE events (
    id SERIAL, 
    event_categories_id integer, 
    name text);

CREATE TABLE event_categories (
    id SERIAL, 
    name text);

CREATE TABLE olympic_games_events (
    olympic_games_id integer, 
    events_id integer, 
    noc_id integer,
    athletes_id integer, 
    athlete_height float, 
    athlete_weight float, 
    athlete_age integer, 
    medal text);
