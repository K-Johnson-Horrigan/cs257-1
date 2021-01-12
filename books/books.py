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
        

parser = argparse.ArgumentParser(description = 'do stuff with books')
parser.add_argument('-a', '--author', help = 'author help statement')
parser.add_argument('-t', '--title', help = 'title help statement')
parser.add_argument('-y', '--year', help = 'year help statement')
arguments = parser.parse_args() 
#print(arguments.author)
print("parsed arguments =", arguments)
#print(arguments.phrase)
#print(arguments.author)


# key is author name, value is set of author's books 
# {author : (title, title, ..), author: (title), ...}
resultsDict = defaultdict(set)

if arguments.author != None:
    searchA = arguments.author
    print("Author search phrase:", searchA)
    # search authors for the phrase
    for book in bookList:
        name = book[2] 
        result = re.search(searchA, name, re.IGNORECASE)
        if result != None:
            # add author to result dict (if they're not already in)
            # and add the book and its year to their list of books 
            resultsDict[book[2]].add(book[0] + ", " + book[1])

if arguments.title != None:
    searchT = arguments.title
    print("Title search phrase:", searchT)
    # search titles for the phrase
    for book in bookList:
        name = book[0] 
        result = re.search(searchT, name, re.IGNORECASE)
        if result != None:
            # add author to result dict (if they're not already in)
            # and add the book to their list of books 
            resultsDict[book[2]].add(book[0] + ", " + book[1])

if arguments.year != None:
    searchY = arguments.year
    print("Year search range:", searchY)
    y1 = searchY[:4]
    y2 = searchY[-4:]
    for book in bookList:
        year = book[1]
        if (y1 <= year) and (year <= y2):
            resultsDict[book[2]].add(book[0] + ", " + book[1])


resultAuthors = resultsDict.keys()
if len(resultAuthors) == 0:
    print("No results")
else:
    for key in resultsDict.keys():
        print(key)
        for title in resultsDict[key]:
            print("    ", title)

print()
print(resultsDict.keys())