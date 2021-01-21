# Books CLI
# CS257 
# Martin Bernard and Antonia Ritter
# Jan 15 2021 

import re
import csv 
import argparse
from collections import defaultdict

#Returns a list of books from books.csv 
def read_csv(): 
    filename = 'books.csv'

    # list of lists
    # each sublist is [title, year, author]
    bookList = []

    # opening the CSV file 
    with open(filename, mode ='r') as file: 
        csvFile = csv.reader(file) 
        for line in csvFile: 
                bookList.append(line)
    
    return bookList
        


# parse arguments and return a list of arguments 
def parse_arguments():
    parser = argparse.ArgumentParser(description = 'Search for books from books.csv given a string of an author, title, and a range of publication years')
    parser.add_argument('-a', '--author', help = 'Phrase to search for in author names, in quotes if multiple words.')
    parser.add_argument('-t', '--title', help = 'Phrase to search for in title, in quotes if multiple words.')
    parser.add_argument('-y', '--year', help = 'Two full years separated by hyphen or a single year. Ex: 1900-2000 Ex2: 2005')
    parser.add_argument('extras', nargs=argparse.REMAINDER) # accounts for unexpected syntax, so usage statement prints 
    arguments = parser.parse_args() 
    return arguments 



def year_in_range(year, year_range):
    """
    Helper for find_matches 
    Input: A range or single year (arguments.year) and a publication year
        Ex. 
            year_in_range(2000, 1995-2000) -> True 
            year_in_range(1975, 2005) -> False 
    Output: True or False depending on whether the range contains the year 
    """

    #if range is a single year
    if len(year_range)==4:
        start_year = year_range 
        end_year = year_range
    #range is two years
    else:
        start_year = year_range[:4]
        end_year = year_range[-4:]
    if (start_year <= year) and (year <= end_year):
        return True
    else:
        return False



def find_matches(arguments):
    """
    Input: List of arguments (the output from parseArgument())
    Output: Default dictionary of books matching the arguments
    """

    # key is author name, value is set of author's books 
    # {author : (title, title, ..), author: (title), ...}
    matched_books = defaultdict(list)

    list_of_books = read_csv()

    for book in list_of_books:

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
            if year_in_range(book[1], arguments.year):
                year = True
            else:
                year = False 
        else:
            year = True  

        # if the author, title, and year all match (or don't exist)
        if author and title and year: 
            # add book to matched_books 
            matched_books[book[2]].append(book[0] + ", " + book[1])
    
    return matched_books



def print_output(arguments, resultDict):
    """
    Input: parsed arguments and a dictionary of books
    Prints usage statement if there are no arguments
    Prints books otherwise 
    """

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
    arguments = parse_arguments()
    matches = find_matches(arguments)
    print_output(arguments, matches)

main()
