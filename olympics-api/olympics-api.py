# olympics-api.py
# Claire Williams and Antonia Ritter
# Feb 2 2021

import flask
import json
import psycopg2
from collections import defaultdict 

app = flask.Flask(__name__)


def query_database(query):
    '''
    Given an SQL query, returns a list of results 
    '''
    from config import password
    from config import user

    # Connect to the database
    try:
        connection = psycopg2.connect(database='olympics', user=user, password=password)
    except Exception as e:
        print(e)
        exit()

    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    results = []
    for row in cursor:
        results.append(row) 

    connection.close()
    return results 



@app.route('/games')
def get_games():
    '''
    Returns list of all olympics games in database.
    '''
    query = 'SELECT competition.competition_id, competition.year, competition.season, competition.city \
            FROM competition \
            ORDER BY year;'
    query_results = query_database(query)
    # response = [{id : 4, year : 1900, season = "Summer", city = "..."}, {...}]
    response = []
    for row in query_results:
        game = defaultdict()
        game['id'] = row[0]
        game['year'] = row[1]
        game['season'] = row[2] 
        game['city'] = row[3] 
        response.append(game)

    return json.dumps(response)


@app.route('/nocs')
def get_nocs():
    '''
    Returns a list of all national olympic committees in database.
    '''
    query = 'SELECT committee.abbreviation, committee.region \
            FROM committee \
            ORDER BY committee.abbreviation;'
    query_results = query_database(query)
    response = []
    for row in query_results:
        noc = defaultdict()
        noc['abbreviation'] = row[0]
        noc['name'] = row[1]
        response.append(noc)

    return json.dumps(response)


@app.route('/medalists/games/<games_id>')
def get_medalists(games_id):
    '''
    Returns a list of medalists for specified games,
    and in a certain noc if given.
    '''

    noc = flask.request.args.get('noc')

    query_base = 'SELECT DISTINCT athlete.athlete_id, athlete.athlete_name, athlete.sex, event.sport, \
                event.event_name, athlete_competition_event.medal \
                FROM athlete, event, athlete_competition, athlete_competition_event, competition, committee \
                WHERE athlete.athlete_id = athlete_competition.athlete_id \
                AND athlete_competition.athlete_competition_id = athlete_competition_event.athlete_competition_id \
                AND athlete_competition_event.event_id = event.event_id \
                AND competition.competition_id = athlete_competition.competition_id \
                AND committee.committee_id = athlete_competition.committee_id \
                AND athlete_competition_event.medal IS NOT NULL \
                AND competition.competition_id = %d' % int(games_id)
    query_without_noc = 'ORDER BY athlete.athlete_name;' 

    if noc is not None:
        query_with_noc = 'AND committee.abbreviation = \'%s\' \
                        ORDER BY athlete.athlete_name;' % noc.upper()
        query = query_base + query_with_noc
    else:
        query = query_base + query_without_noc

    query_results = query_database(query)
    response = []
    for row in query_results:
        athletes = defaultdict()
        athletes['athlete_id'] = row[0]
        athletes['athlete_name'] = row[1]
        athletes['athlete_sex'] = row[2]
        athletes['sport'] = row[3]
        athletes['event'] = row[4]
        athletes['medal'] = row[5] 
        response.append(athletes)

    return json.dumps(response)



if __name__ == '__main__':
    host = 'localhost'
    port = 5000 
    app.run(host = host, port = port, debug = True)