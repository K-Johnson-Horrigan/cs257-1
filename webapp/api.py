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
def get_single_production(country, crop, year):
    query = get_single_query(country, crop, year)
    cursor = query_database(query)
    for row in cursor:
        production_number = row
    return json.dumps(production_number)

@api.route('/graphed_production/<country>/<crop>')
def get_graphed_production(country, crop):
    query = get_graph_query(country, crop)
    cursor = query_database(query)
    crops_set = set() 
    cursor_table = []
    for row in cursor: # row is crop, year, production 
        cursor_table.append(row)
        crops_set.add(row[0])
    productions_by_year_dict = {} # {crop: {year: production, year: production, …}, crop: …}
    # create the subdict for each crop individually 
    for crop in crops_set:
        one_crop_dict = {}
        for row in cursor_table:
            if row[0] == crop:
                one_crop_dict[row[1]] = row[2]
        productions_by_year_dict[crop] = one_crop_dict
    return json.dumps(productions_by_year_dict)

@api.route('/tabled_production/<country>/<year>')
def get_tabled_production(country, year):
    query = get_table_query(country, year)
    cursor = query_database(query)
    productions_by_crop_dict = {} # {crop: production, crop: production, ...}
    for row in cursor: 
        productions_by_crop_dict[row[0]] = row[1]
    return json.dumps(productions_by_crop_dict)

@api.route('/mapped_production/<crop>/<year>')
def get_mapped_production(crop, year):
    query = get_map_query(crop, year)
    cursor = query_database(query)
    # format: {USA: {production: 189900, country_name: United States of America}, AUS: {production: 5, country_name: Australia], …}
    productions_by_country_dict = {}
    for row in cursor: # row is country, abbreviation, production 
        country_name = row[0]
        abbreviation = row[1]
        production = row[2]
        if (abbreviation != None and production != None):
            productions_by_country_dict[abbreviation] = {'production': int(production), 'country_name': country_name}
    return json.dumps(productions_by_country_dict)

@api.route('/help')
def get_help():
    return flask.render_template('help.html')

def convert_cursor_to_list(cursor):
    list = []
    for row in cursor:
        list.append(row[0])
    return list


def get_menus_query(key):
    if key == 'countries': query = '''SELECT country FROM countries ORDER BY country'''
    elif key == 'crops': query = '''SELECT crop FROM crops ORDER BY crop'''
    elif key == 'years': query = '''SELECT DISTINCT year FROM country_crop ORDER BY year DESC'''
    return [query]


def get_map_query(crop, year):
    '''Returns query text and search clause tuple in a list'''
    if crop != 'All crops' and year != 'All years':
        query_text = '''SELECT countries.country, countries.abbreviation, country_crop.production \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id \
                        AND country_crop.year = %s \
                        AND crops.crop = %s;'''
        search_clause = (year, crop)
    elif year == 'All years' and crop != 'All crops':
        query_text = '''SELECT countries.country, countries.abbreviation, SUM(country_crop.production) \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id \
                        AND crops.crop = %s \
                        GROUP BY countries.country, countries.abbreviation;'''
        search_clause = (crop, )
    elif year != 'All years' and crop == 'All crops':
        query_text = '''SELECT countries.country, countries.abbreviation, SUM(country_crop.production) \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id \
                        AND country_crop.year = %s \
                        GROUP BY countries.country, countries.abbreviation;'''
        search_clause = (year,)
    elif year == 'All years' and crop == 'All crops':
        query_text = '''SELECT countries.country, countries.abbreviation, SUM(country_crop.production) \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id \
                        GROUP BY countries.country, countries.abbreviation;'''
        search_clause = ()
    return [query_text, search_clause]


def get_single_query(country, crop, year):
    query_text = '''SELECT country_crop.production \
                    FROM countries, crops, country_crop \
                    WHERE countries.id = country_crop.country_id \
                    AND crops.id = country_crop.crop_id \
                    AND countries.country = %s \
                    AND crops.crop = %s \
                    AND country_crop.year = %s;'''
    search_clause = (country, crop, year)
    return [query_text, search_clause]


def get_table_query(country, year):
    query_text = '''SELECT crops.crop, country_crop.production \
                    FROM countries, crops, country_crop \
                    WHERE crops.id = country_crop.crop_id \
                    AND countries.id = country_crop.country_id \
                    AND countries.country = %s
                    AND country_crop.year = %s ORDER BY country_crop.production DESC;'''
    search_clause = (country, year)
    return [query_text, search_clause]


def get_graph_query(country, crop):
    if crop != 'All crops':
        query_text = '''SELECT crops.crop, country_crop.year, country_crop.production \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id \
                        AND countries.country = %s \
                        AND crops.crop = %s;'''
        search_clause = (country, crop)
    elif crop == 'All crops':
        query_text = '''SELECT crops.crop, country_crop.year, country_crop.production \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id \
                        AND countries.country = %s;'''
        search_clause = (country,)
    return [query_text, search_clause]


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
