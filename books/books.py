# Books CLI
# CS257 
# Martin Bernard and Antonia Ritter
# Jan 15 2021 

import re
import csv 
import argparse
from collections import defaultdict


filename = 'books.csv'

# list of lists
# each sublist is [title, year, author]
bookList = []

# opening the CSV file 
with open(filename, mode ='r') as file:     
       # reading the CSV file 
       csvFile = csv.reader(file) 
       # displaying the contents of the CSV file 
       for line in csvFile: 
            bookList.append(line)
        

# parse arguments 
def parseArguments():
    parser = argparse.ArgumentParser(description = 'do stuff with books')
    parser.add_argument('-a', '--author', help = 'Phrase to search for in author names, in quotes if multiple words.')
    parser.add_argument('-t', '--title', help = 'Phrase to search for in title, in quotes if multiple words.')
    parser.add_argument('-y', '--year', help = 'Two full years separated by hypen. Ex: 1900-2000')
    arguments = parser.parse_args() 
    #print("parsed arguments =", arguments)
    return arguments 


# takes a phrase, returns dict with matching authors 
def getAuthors(searchA):
    # key is author name, value is set of author's books
    returnDict = defaultdict(set)
    # search authors for the phrase
    for book in bookList:
        name = book[2] 
        result = re.search(searchA, name, re.IGNORECASE)
        if result != None:
            # add author to result dict (if they're not already in)
            # and add the book and its year to their list of books 
            returnDict[book[2]].add(book[0] + ", " + book[1])
    return returnDict 


def getTitles(searchT):
    returnDict = defaultdict(set)
    for book in bookList:
        name = book[0] 
        result = re.search(searchT, name, re.IGNORECASE)
        if result != None:
            returnDict[book[2]].add(book[0] + ", " + book[1])
    return returnDict


def getYears(searchY):
    returnDict = defaultdict(set)
    #user only typed in one year 
    if len(searchY)==4:
        y1 = searchY
        y2 = searchY
    #user entered year range
    else: 
        y1 = searchY[:4]
        y2 = searchY[-4:]
    for book in bookList:
        year = book[1]
        if (y1 <= year) and (year <= y2):
            returnDict[book[2]].add(book[0] + ", " + book[1])
    return returnDict



arguments = parseArguments()

# key is author name, value is set of author's books 
# {author : (title, title, ..), author: (title), ...}
resultsDict = defaultdict(set)

if arguments.author != None:
    authorDict = getAuthors(arguments.author)
    for key in authorDict.keys():
        resultsDict[key] = authorDict[key]

if arguments.title != None:
    titleDict = getTitles(arguments.title)
    for key in titleDict.keys():
        resultsDict[key] = titleDict[key]

if arguments.year != None:
    yearDict = getYears(arguments.year)
    for key in yearDict.keys():
        resultsDict[key] = yearDict[key]


 

# print out results 
resultAuthors = resultsDict.keys()
if len(resultAuthors) == 0:
    print("No results")
else:
    for key in resultsDict.keys():
        print()
        print(key)
        for title in resultsDict[key]:
            print("    ", title)
