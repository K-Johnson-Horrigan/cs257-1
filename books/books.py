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
       csvFile = csv.reader(file) 
       for line in csvFile: 
            bookList.append(line)
        

# parse arguments and return a list of arguments 
def parseArguments():
    parser = argparse.ArgumentParser(description = 'Search for books from books.csv given a string of an author, title, and a range of publication years')
    parser.add_argument('-a', '--author', help = 'Phrase to search for in author names, in quotes if multiple words.')
    parser.add_argument('-t', '--title', help = 'Phrase to search for in title, in quotes if multiple words.')
    parser.add_argument('-y', '--year', help = 'Two full years separated by hyphen or a single year. Ex: 1900-2000 Ex2: 2005')
    parser.add_argument('extras', nargs=argparse.REMAINDER) # accounts for unexpected syntax, so usage statement prints 
    arguments = parser.parse_args() 
    return arguments 


"""
    Helper for findMatches 
    Input: A range or single year (arguments.year) and a publication year 
    Output: True or False depending on whether the range contains the year 
"""
def yearMatch(searchY, year):
    #single year
    if len(searchY)==4:
        y1 = searchY
        y2 = searchY
    #year range
    else:
        y1 = searchY[:4]
        y2 = searchY[-4:]
    if (y1 <= year) and (year <= y2):
        return True
    else:
        return False


"""
    Input: List of arguments (the output from parseArgument())
    Output: Default dictionary of books matching the arguments
"""
def findMatches(arguments):

    # key is author name, value is set of author's books 
    # {author : (title, title, ..), author: (title), ...}
    reDict = defaultdict(list)

    for book in bookList:

        # author 
        if arguments.author != None: # author is specified 
            if (re.search(arguments.author, book[2], re.IGNORECASE)): # there is a match
                author = True
            else: # there is no match 
                author = False 
        else: # no author specified 
            author = True 

        # title 
        if arguments.title != None:
            if (re.search(arguments.title, book[0], re.IGNORECASE)):
                title = True
            else:
                title = False 
        else: 
            title = True 

        # year 
        if (arguments.year != None):
            if yearMatch(arguments.year, book[1]):
                year = True
            else:
                year = False 
        else:
            year = True  

        # if the author, title, and year all match (or don't exist)
        if author and title and year: 
            # add book to reDict 
            reDict[book[2]].append(book[0] + ", " + book[1])
    
    return reDict


"""
    Input: parsed arguments and a dictionary of books
    Prints usage statement if there are no arguments
    Prints books otherwise 
"""
def printOutput(arguments, resultDict):
    # if no arguments given
    if arguments.author == None and arguments.title == None and arguments.year == None:
        with open("usage.txt","r") as f:
            for line in f:
                print(line.rstrip())
    else:
        # print out results 
        resultAuthors = resultDict.keys()
        if len(resultAuthors) == 0:
            print("No results")
        else:
            for key in sorted(resultDict.keys()):
                print()
                print(key)
                for title in resultDict[key]:
                    print("    ", title)


def main():
    arguments = parseArguments()
    matches = findMatches(arguments)
    printOutput(arguments, matches)

main()
