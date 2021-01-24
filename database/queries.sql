SELECT * 
FROM committee
ORDER BY abbreviation;

-- List the names of all the athletes from Kenya. If your database design allows it, sort the athletes by last name.
SELECT athlete.athlete_name 
FROM athlete, committee, athlete_competition
WHERE athlete.athlete_id = athlete_competition.athlete_id
AND athlete_competition.committee_id = committee.committee_id
AND committee.region = 'Kenya'
ORDER BY athlete.athlete_name; 

-- List all the medals won by Greg Louganis, sorted by year. Include whatever fields in this output that you think appropriate.
SELECT athlete_competition_event.medal, competition.competition_name
FROM athlete, athlete_competition, competition, athlete_competition_event
WHERE athlete.athlete_id = athlete_competition.athlete_id 
AND athlete_competition.competition_id = competition.competition_id
AND athlete_competition.athlete_competition_id = athlete_competition_event.athlete_competition_id
AND athlete.athlete_name = 'Greg Louganis';

-- List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.
SELECT committee.region, COUNT(athlete_competition_event.medal)
FROM committee, athlete_competition, athlete_competition_event
WHERE committee.committee_id = athlete_competition.committee_id 
AND athlete_competition.athlete_competition_id = athlete_competition_event.athlete_competition_id
AND athlete_competition_event.medal = 'Gold'
GROUP BY  committee.region
ORDER BY COUNT(athlete_competition_event.medal) DESC;