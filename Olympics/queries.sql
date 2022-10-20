SELECT * FROM noc_reg
ORDER BY noc_reg.noc;

SELECT DISTINCT athlete.name
FROM athlete, athlete_year, noc_reg
WHERE noc_reg.team = 'Jamaica'
AND noc_reg.id = athlete_year.noc_reg_id
AND athlete_year.athlete_id = athlete.id;


'''List all the NOCs (National Olympic Committees), in alphabetical order by abbreviation. These entities, by the way, are mostly equivalent to countries. But in some cases, you might find that a portion of a country participated in a particular games (e.g. one guy from Newfoundland in 1904) or some other oddball situation.'''

SELECT noc.noc_abreviation
FROM noc
ORDER BY noc.noc_abreviation ASC;

'''List the names of all the athletes from Jamaica. If your database design allows it, sort the athletes by last name.'''

SELECT DISTINCT athletes.athlete_name
FROM athletes, noc, results
WHERE athletes.id = results.athlete_id
AND noc.id = results.noc_id
AND noc.noc_region = 'Jamaica';

'''List all the medals won by Greg Louganis, sorted by year. Include whatever fields in this output that you think appropriate. Going from most recent games to past'''

ORDER BY games.game_year DESC

'''List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.'''

SELECT COUNT(results.medal), noc.noc_region
FROM noc, results
WHERE noc.id = results.team_id
AND event_results.medal = 'Gold'
GROUP BY nocs.name
ORDER BY COUNT(event_results.medal) DESC;

