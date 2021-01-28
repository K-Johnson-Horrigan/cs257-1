# olympics.py
# CS257 
# Jan 29 2021
# Antonia Ritter


import psycopg2
import sys
from tabulate import tabulate



# returns list of command line arguments 
def parse_arguments():
    arguments = sys.argv
    return arguments 



def construct_noc_query(noc):
    """
    Given a national olympic committee abbreviation, 
    returns an SQL query to list all the athletes from that noc. 
    """
    query = 'SELECT DISTINCT athlete.athlete_name \
            FROM athlete, committee, athlete_competition \
            WHERE athlete.athlete_id = athlete_competition.athlete_id \
            AND athlete_competition.committee_id = committee.committee_id \
            AND committee.abbreviation = \'%s\' \
            ORDER BY athlete.athlete_name;' % noc 

    return query 



def construct_medal_query():
    """
    Returns an SQL query to list all NOCs and number of gold medals won, 
    in decreasing order of the number of gold medals.
    """ 
    query = 'SELECT committee.abbreviation, COUNT(athlete_competition_event.medal) \
            FROM committee, athlete_competition, athlete_competition_event \
            WHERE committee.committee_id = athlete_competition.committee_id \
            AND athlete_competition.athlete_competition_id = athlete_competition_event.athlete_competition_id \
            AND athlete_competition_event.medal = \'Gold\' \
            GROUP BY committee.abbreviation \
            ORDER BY COUNT(athlete_competition_event.medal) DESC;'

    return query 



def construct_athlete_query(name):
    """
    Given the name of an athlete, returns an SQL query to print out
    information about that athlete. 
    """
    query = 'SELECT DISTINCT athlete.athlete_name, competition.competition_name, event.event_name, \
            committee.region, athlete_competition_event.medal \
            FROM athlete, athlete_competition, competition, event, athlete_competition_event, committee \
            WHERE athlete.athlete_id = athlete_competition.athlete_id \
            AND competition.competition_id = athlete_competition.competition_id \
            AND athlete_competition.athlete_competition_id = athlete_competition_event.athlete_competition_id \
            AND athlete_competition_event.event_id = event.event_id \
            AND committee.committee_id = athlete_competition.committee_id \
            AND athlete.athlete_name LIKE \'%' + str(name) + '%\' ORDER BY athlete.athlete_name, competition.competition_name;'

    return query 



def construct_query(arguments):
    """
    Given command line arguments, 
    returns an SQL query or None 
    """

    usage_statement = '\nUsage Statement for olympics.py: \n\n\
    -c, --committee NOC:  list all athletes from the specified NOC (by abbreviation; case-sensitive) \n\
    -m, --medals:           list all NOCs and number of gold medals won \n\
    -a, -athlete "name":    prints details about specified athlete (case-sensitive) \n\
    -h, --help:             print this usage statement \n\n\
    Ex: python3 olympics.py -a \"Gregory E\" \n\
    Ex: python3 olympics.py -c DEN \n'

    missing_argument_message = 'Error: Please enter second argument or type \"python3 olympics.py --help\" for help.'

    # get first argument or error-catch 
    if len(arguments) < 2:
        print(usage_statement) 
        return None 
    else:
        flag = arguments[1] 
        
    if flag == '-h' or flag == '--help':
        print(usage_statement)
        return None 

    elif flag == '-c' or flag == '--committee':
        # check if there's a second input
        if len(arguments)<3:
            print(missing_argument_message)
            return None 
        else: 
            query = construct_noc_query(arguments[2]) 

    elif flag == '-m' or flag == '--medals':
        query = construct_medal_query() 

    elif flag == '-a' or flag == '--athlete':
        if len(arguments)<3:
            print(missing_argument_message)
            return None 
        else: 
            query = construct_athlete_query(arguments[2]) 

    # if syntax is wrong or unknown argument used 
    else: 
        print(usage_statement) 
        return None 

    return query 



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

    # Query the database, create cursor 
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



def print_results(arguments, results):
    """
    Takes lists of command line arguments and results 
    (the outputs from parse_arguments and query_database)
    and prints them in pleasing tables 
    """

    # if arguments[1] doesn't exist, query=None and this function isn't called 
    flag = arguments[1] 

    if flag == '-c' or flag == '--committee':
        header = 'Athletes from ' + arguments[2]
        print(tabulate(results, headers = [header], tablefmt='psql'))
        
    elif flag == '-m' or flag == '--medals':
        print(tabulate(results, headers = ['Committee', 'Gold Medals'], tablefmt='psql', colalign=('left','left')))

    elif flag == '-a' or flag == '--athlete':
        print(tabulate(results, headers = ['Name', 'Competition', 'Event', 'NOC', 'Medal'], tablefmt='psql'))



def main():
    arguments = parse_arguments() 
    query = construct_query(arguments) 
    if query != None:
        results = query_database(query) 
        print_results(arguments, results) 


if __name__ == '__main__':
    main() 