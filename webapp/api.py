# Authors: Antonia Ritter and Kai Johnson
# CS257
# Feb-Mar 2021

import flask
import json
import sys
import psycopg2
from config import database, user, password
from collections import defaultdict


api = flask.Blueprint('api', __name__)


@api.route('/menus/')
def get_menus():
    '''Returns a JSON dictionary of with keys category name
       and values lists of all elements for that category.
    '''
    menus = {'countries' : [], 'crops' : [], 'years' : []}
    for category in menus.keys():
        query_text, search_clause = get_menus_query(category)
        cursor = query_database(query_text, search_clause)
        menu_list = []
        for row in cursor:
            menu_list.append(row[0])
        menu_list.insert(0, ('All ' + category)) # add "All" option to the top of menus
        menus[category] = menu_list
    return json.dumps(menus)


@api.route('/single_production/<country>/<crop>/<year>')
def get_single_production(country, crop, year):
    '''Returns a JSON of a single integer.'''
    query_text, search_clause = get_single_query(country, crop, year)
    cursor = query_database(query_text, search_clause)
    for row in cursor:
        production = row
    return json.dumps(production)


@api.route('/graphed_production/<country>/<crop>')
def get_graphed_production(country, crop):
    '''Returns a JSON of a dictionary of dictionaries in the format:
       {crop: {year: production}}
    '''
    query_text, search_clause = get_graph_query(country, crop)
    cursor = query_database(query_text, search_clause)
    production_by_crop_year_dict = {}
    for row in cursor:
        crop = row[0]
        year = row[1]
        production = row[2]
        if crop in production_by_crop_year_dict:
            production_by_crop_year_dict[crop][year] = production
        else:
            production_by_crop_year_dict[crop] = {year : production}
    return json.dumps(production_by_crop_year_dict)


@api.route('/charted_production/<country>/<year>')
def get_charted_production(country, year):
    '''Returns a JSON of a 2D list in the format:
       [[crop, production], [crop, production], ...]
    '''
    query_text, search_clause = get_chart_query(country, year)
    cursor = query_database(query_text, search_clause)
    productions_by_crop_list = []
    for row in cursor:
        crop = row[0]
        production = row[1]
        if production != None:
            productions_by_crop_list.append([crop, production])
    return json.dumps(productions_by_crop_list)


@api.route('/mapped_production/<crop>/<year>')
def get_mapped_production(crop, year):
    '''Returns a JSON of a dictionary of dictionaries in the format:
       {USA: {production: 189900, country_name: United States of America}, AUS: {production: 5, country_name: Australia], …}
    '''
    query_text, search_clause = get_map_query(crop, year)
    cursor = query_database(query_text, search_clause)
    productions_by_country_dict = {}
    for row in cursor:
        country_name = row[0]
        abbreviation = row[1]
        production = row[2]
        if abbreviation != None and production != None:
            productions_by_country_dict[abbreviation] = {'production': int(production), 'country_name': country_name}
    return json.dumps(productions_by_country_dict)


@api.route('/help')
def get_help():
    '''Returns the help.html page'''
    return flask.render_template('help.html')

def get_menus_query(key):
    '''Returns query text and search clause tuple (there isn't one) for get_menus'''
    if key == 'countries': query_text = '''SELECT country FROM countries ORDER BY country'''
    elif key == 'crops': query_text = '''SELECT crop FROM crops ORDER BY crop'''
    elif key == 'years': query_text = '''SELECT DISTINCT year FROM country_crop ORDER BY year DESC'''
    return query_text, None


def get_map_query(crop, year):
    '''Returns query text and search clause tuple for mapped_production'''
    if crop != 'All crops' and year != 'All years':
        query_text = '''SELECT countries.country, countries.abbreviation, country_crop.production \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id \
                        AND country_crop.year = %s \
                        AND crops.crop = %s
                        ORDER BY country_crop.production DESC;'''
        search_clause = (year, crop)
    elif year == 'All years' and crop != 'All crops':
        query_text = '''SELECT countries.country, countries.abbreviation, SUM(country_crop.production) AS production \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id \
                        AND crops.crop = %s \
                        GROUP BY countries.country, countries.abbreviation
                        ORDER BY production DESC;'''
        search_clause = (crop, )
    elif year != 'All years' and crop == 'All crops':
        query_text = '''SELECT countries.country, countries.abbreviation, SUM(country_crop.production) AS production \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id \
                        AND country_crop.year = %s \
                        GROUP BY countries.country, countries.abbreviation
                        ORDER BY production DESC;'''
        search_clause = (year,)
    elif year == 'All years' and crop == 'All crops':
        query_text = '''SELECT countries.country, countries.abbreviation, SUM(country_crop.production) AS production \
                        FROM countries, crops, country_crop \
                        WHERE crops.id = country_crop.crop_id \
                        AND countries.id = country_crop.country_id \
                        GROUP BY countries.country, countries.abbreviation \
                        ORDER BY production DESC;'''
        search_clause = ()
    return query_text, search_clause


def get_single_query(country, crop, year):
    '''Returns query text and search clause tuple for single_production'''
    query_text = '''SELECT country_crop.production \
                    FROM countries, crops, country_crop \
                    WHERE countries.id = country_crop.country_id \
                    AND crops.id = country_crop.crop_id \
                    AND countries.country = %s \
                    AND crops.crop = %s \
                    AND country_crop.year = %s;'''
    search_clause = (country, crop, year)
    return query_text, search_clause


def get_chart_query(country, year):
    '''Returns query text and search clause tuple for charted_production'''
    query_text = '''SELECT crops.crop, country_crop.production \
                    FROM countries, crops, country_crop \
                    WHERE crops.id = country_crop.crop_id \
                    AND countries.id = country_crop.country_id \
                    AND countries.country = %s
                    AND country_crop.year = %s ORDER BY country_crop.production DESC;'''
    search_clause = (country, year)
    return query_text, search_clause


def get_graph_query(country, crop):
    '''Returns query text and search clause tuple for graphed_production'''
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
    return query_text, search_clause


def query_database(query_text, search_clause):
    '''Executes the passed query and returns the resulting cursor or prints an error message and returns an empty string if the query failed.'''
    connection = get_database_connection()
    cursor = ""
    try:
        cursor = connection.cursor()
        if search_clause:
            cursor.execute(query_text, search_clause)
        else:
            cursor.execute(query_text)
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
