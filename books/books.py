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

    #For each book check to see if it matches the arguments and add it to the dictionary if it matches
    for book in bookList:

        #Add books only if it matches the author, title, and if in range of publication year
        if (authorBool and titleBool and yearBool and (re.search(arguments.author, book[2], re.IGNORECASE)) 
            and (re.search(arguments.title, book[0], re.IGNORECASE)) and yearMatch(arguments.year, book[1])):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Author and title 
        elif (authorBool and titleBool and not yearBool and (re.search(arguments.author, book[2], re.IGNORECASE)) 
            and (re.search(arguments.title, book[0], re.IGNORECASE))):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Author and year
        elif (authorBool and yearBool and not titleBool and (re.search(arguments.author, book[2], re.IGNORECASE)) 
            and yearMatch(arguments.year, book[1])):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Title and year
        elif (titleBool and yearBool and not authorBool and (re.search(arguments.title, book[0], re.IGNORECASE)) 
            and yearMatch(arguments.year, book[1])):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Author 
        elif (authorBool and not titleBool and not yearBool and (re.search(arguments.author, book[2], re.IGNORECASE))):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Title 
        elif (titleBool and not authorBool and not yearBool and (re.search(arguments.title, book[0], re.IGNORECASE))):
            resultsDict[book[2]].add(book[0] + ", " + book[1])

        #Year
        elif (yearBool and not authorBool and not titleBool and yearMatch(arguments.year, book[1])):
            resultsDict[book[2]].add(book[0] + ", " + book[1])
    
    return resultsDict


"""
    Input: parsed arguments and a dictionary of books
    Prints usage statement if there are no arguments
    Prints books otherwise 
"""
def printOutput(arguments, resultDict):
    if arguments.author == None and arguments.title == None and arguments.year == None:
        with open("usage.txt","r") as f:
            for line in f:
                print(line.rstrip())
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


def main():
    arguments = parseArguments()
    printOutput(arguments, multi_arguments(arguments))

main()
