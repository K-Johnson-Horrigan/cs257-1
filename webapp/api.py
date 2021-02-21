#Authors: Antonia Ritter and Kai Johnson

import flask
import json
import sys
import psycopg2
from config import database, user, password

api = flask.Blueprint('api', __name__)

@api.route('/menus/')
def get_menus():
    menus = {'countries' : [], 'crops' : [], 'years' : []}
    
    for key in menus.keys():
        query = get_menus_query(key)
        cursor = query_database(query)
        menu_list = convert_cursor_to_list(cursor)
        menu_list.insert(0, ('All ' + key))
        menus[key] = menu_list

    return json.dumps([menus])


@api.route('/main/<country>')
def get_results(country):
    #country = flask.request.args.get('country', default='spain')
    if country == 'All countries':
        results = ["realllly lots"]
        print('all countries~~~')

    else: results = ["lots"]
    results = [country]
    results = ["lots"]
    return json.dumps(results)

def convert_cursor_to_list(cursor):
    list = []
    for row in cursor:
        list.append(row[0])
    return list

def get_menus_query(key):
    if key == 'countries': query = '''SELECT country FROM countries ORDER BY country'''
    elif key == 'crops': query = '''SELECT crop FROM crops ORDER BY crop'''
    elif key == 'years': query = '''SELECT DISTINCT year FROM country_crop ORDER BY year'''
    return [query]

def query_database(query):
    '''Executes the passed query and returns the resulting cursor or prints an error message and returns an empty string if the query failed.'''
    connection = get_database_connection()
    cursor = ""
    try:
        cursor = connection.cursor()
        cursor.execute(query[0])
    except Exception as e:
        print(e)
    return cursor

def get_database_connection():
    '''Returns a connection to a database specified by 'config.py'.'''
    connection = ""
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
    return connection
