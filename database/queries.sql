SELECT * 
FROM committee
ORDER BY abbreviation;

SELECT DISTINCT athlete.athlete_name 
FROM athlete, committee, athlete_competition
WHERE athlete.athlete_id = athlete_competition.athlete_id
AND athlete_competition.committee_id = committee.committee_id
AND committee.region = 'Kenya'
ORDER BY athlete.athlete_name; 

SELECT athlete_competition_event.medal, competition.competition_name, athlete.athlete_name, event.event_name
FROM athlete, athlete_competition, competition, athlete_competition_event, event
WHERE athlete.athlete_id = athlete_competition.athlete_id 
AND athlete_competition.competition_id = competition.competition_id
AND athlete_competition.athlete_competition_id = athlete_competition_event.athlete_competition_id
AND athlete_competition_event.event_id = event.event_id
AND athlete_competition_event.medal IS NOT NULL
AND athlete.athlete_name LIKE '%"Greg" Louganis'
ORDER BY competition.competition_name;

SELECT committee.region, COUNT(athlete_competition_event.medal)
FROM committee, athlete_competition, athlete_competition_event
WHERE committee.committee_id = athlete_competition.committee_id 
AND athlete_competition.athlete_competition_id = athlete_competition_event.athlete_competition_id
AND athlete_competition_event.medal = 'Gold'
GROUP BY  committee.region
ORDER BY COUNT(athlete_competition_event.medal) DESC;