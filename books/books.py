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
    parser = argparse.ArgumentParser(description = 'Search for books from books.csv given a string of an author, title, and a range of publication years')
    parser.add_argument('-a', '--author', help = 'Phrase to search for in author names, in quotes if multiple words.')
    parser.add_argument('-t', '--title', help = 'Phrase to search for in title, in quotes if multiple words.')
    parser.add_argument('-y', '--year', help = 'Two full years separated by hypen. Ex: 1900-2000')
    arguments = parser.parse_args() 
    #print("parsed arguments =", arguments)
    return arguments 

# searchY is argument.year, year is publication date of book
# returns True if year is in searchY, or False if not
# yearMatch(2000-2001, 1900) -> Flase
def yearMatch(searchY, year):
    #user only typed in one year
    if len(searchY)==4:
        y1 = searchY
        y2 = searchY
    #user entered year range
    else:
        y1 = searchY[:4]
        y2 = searchY[-4:]
    if (y1 <= year) and (year <= y2):
        return True
    else:
        return False

def multi_arguments(arguments):
    # key is author name, value is set of author's books 
    # {author : (title, title, ..), author: (title), ...}
    resultsDict = defaultdict(set)

    authorBool = False
    titleBool = False
    yearBool = False

    if arguments.author != None:
        authorBool = True
    if arguments.title != None:
        titleBool = True
    if arguments.year != None:
        yearBool = True

    for book in bookList:
        #Arguments for author, title, and year
        if (authorBool and titleBool and yearBool and (re.search(arguments.author, book[2], re.IGNORECASE)) 
            and (re.search(arguments.title, book[0], re.IGNORECASE)) and yearMatch(arguments.year, book[1])):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Arguments for author and title 
        elif (authorBool and titleBool and not yearBool and (re.search(arguments.author, book[2], re.IGNORECASE)) 
            and (re.search(arguments.title, book[0], re.IGNORECASE))):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Arguments for author and year
        elif (authorBool and yearBool and not titleBool and (re.search(arguments.author, book[2], re.IGNORECASE)) 
            and yearMatch(arguments.year, book[1])):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Arguments for title and year
        elif (titleBool and yearBool and not authorBool and (re.search(arguments.author, book[0], re.IGNORECASE)) 
            and yearMatch(arguments.year, book[1])):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Arguments for author 
        elif (authorBool and not titleBool and not yearBool and (re.search(arguments.author, book[2], re.IGNORECASE))):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Arguments for title 
        elif (titleBool and not authorBool and not yearBool and (re.search(arguments.title, book[0], re.IGNORECASE))):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Arguments for year
        elif (yearBool and not authorBool and not titleBool and yearMatch(arguments.year, book[1])):
            resultsDict[book[2]].add(book[0] + ", " + book[1])
    
    return resultsDict


arguments = parseArguments()

if arguments.author == None and arguments.title == None and arguments.year == None:
    with open("usage.txt","r") as f:
        for line in f:
            print(line, "\b")
else:
    resultDict = multi_arguments(arguments)

    # print out results 
    resultAuthors = resultDict.keys()
    if len(resultAuthors) == 0:
        print("No results")
    else:
        for key in resultDict.keys():
            print()
            print(key)
            for title in resultDict[key]:
                print("    ", title)
