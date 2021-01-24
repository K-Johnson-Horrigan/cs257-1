CREATE TABLE athlete (
    athlete_id SERIAL,
    athlete_name text,
    age integer,
    height integer,
    weight integer, 
    sex text
); 

CREATE TABLE committee (
    committee_id SERIAL,
    region text,
    abbreviation text,
    notes text
);

CREATE TABLE competition (
    competition_id SERIAL,
    year integer,
    season text,
    city text
    competition_name text
);

CREATE TABLE event (
    event_id SERIAL,
    event_name text,
    sport text
);

CREATE TABLE athlete_competition (
    athlete_competition_id SERIAL,
    athlete_id integer,
    competition_id integer,
    committee_id integer
);

CREATE TABLE athlete_competition_event (
    athlete_competition_id integer,
    event_id integer,
    medal text
);
