import flask
import json
import sys
import psycopg2
from config import database, user, password
from collections import defaultdict

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

@api.route('/single_production/<country>/<crop>/<year>')
def get_single_results(country, crop, year):
    result = 800
    return json.dumps(result)

@api.route('/graphed_production/<country>/<crop>')
def get_graphed_production_results(country, crop):
    dict = {"soybeans": {1999: 666, 2000: 1000}, "maize": {1999: 100, 2000: 200}}
    return json.dumps(dict)

@api.route('/tabled_production/<country>/<year>')
def get_tabled_production_results(country, year):
    dict = {"soybeans": 666, "maize": 100}
    return json.dumps(dict)

@api.route('/mapped_production/<crop>/<year>')
def get_mapped_production(crop, year):
    query = get_map_query(crop, year)
    cursor = query_database(query)
    yields_by_country_dict = {}
    for row in cursor:
        yields_by_country_dict[row[0]] = row[1]
    return json.dumps(yields_by_country_dict)

def get_map_query(crop, year):
    '''Returns query text and search clause tuple in a list'''
    if crop != 'All' and year != 'All':
        query = '''SELECT countries.country, country_crop.yield
                FROM countries, crops, country_crop
                WHERE crops.id = country_crop.crop_id
                AND countries.id = country_crop.country_id
                AND country_crop.year = %s
                AND crops.crop = %s;'''
        search_clause = (year, crop)
    '''
    else:
        query_beginning = 'SELECT countries.country, SUM(country_crop.yield) \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id'
        query_end = 'GROUP BY countries.country;'
        if year == 'All' and crop != 'All':
            query_middle = 'AND crops.crop = \'%s\''
            search_clause = (crop,)
        elif year != 'All' and crop == 'All':
            query_middle = 'AND country_crop.year = %d'
            search_clause - (year,)
        elif year == 'All' and crop == 'All':
            query_middle = ''
            search_clause = ()
        query = query_beginning + query_middle + query_end
    '''
    return [query, search_clause]

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
        if len(query)==2:
            cursor.execute(query[0], query[1])
        else: cursor.execute(query[0])
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
