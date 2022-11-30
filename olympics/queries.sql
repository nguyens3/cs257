--List all the NOCs (National Olympic Committees), in alphabetical order by abbreviation. 
--These entities, by the way, are mostly equivalent to countries. 
--But in some cases, you might find that a portion of a country participated in a particular games (e.g. one guy from Newfoundland in 1904) or some other oddball situation
SELECT noc.abbreviation
FROM NOC
ORDER BY noc.abbreviation;

--List the names of all the athletes from Jamaica. 
--If your database design allows it, sort the athletes by last name.
--NOTE: unable to sort athletes by last name since the athletes name is grouped into a single column. 
SELECT DISTINCT athletes.name
FROM athletes, NOC, olympic_games_events
WHERE athletes.id = olympic_games_events.athletes_id
AND noc.id = olympic_games_events.noc_id
AND noc.region = 'Jamaica';

--List all the medals won by Greg Louganis, sorted by year. 
--Include whatever fields in this output that you think appropriate. 
SELECT olympic_games_events.medal, olympic_games.year, olympic_games.season, events.name, noc.abbreviation
FROM athletes, olympic_games, events, noc,  olympic_games_events
WHERE athletes.id = olympic_games_events.athletes_id
AND olympic_games.id = olympic_games_events.olympic_games_id
AND events.id = olympic_games_events.events_id
AND noc.id = olympic_games_events.noc_id
AND athletes.name LIKE 'Greg%Louganis'
ORDER BY olympic_games.year;

--List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.
SELECT noc.abbreviation, olympic_games_events.medal, COUNT(olympic_games_events.medal)
FROM noc, olympic_games_events
WHERE noc.id = olympic_games_events.noc_id
AND olympic_games_events.medal = 'Gold'
GROUP BY noc.abbreviation, olympic_games_events.medal
ORDER BY COUNT(olympic_games_events.medal) DESC;





