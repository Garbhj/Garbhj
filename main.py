# ************************************************************************
# Jason Hu
# Assignment 2 - CIA Fact Finder
# Computer Science 30 IB
# 10/28/2022

# This program is my own work - J.H */

# FEATURES:
# - This program lets you search a file containing 256 countries and territories with data regarding Population,
# GDP (PPP), Unemployment Rate (%),  Birth Rate (per 1000 people), area (km^2), and life expectancy.
# - You can search the list of countries by entering a string, and it will produce a list of countries with names that
# contain the string.
# - You can also enter a column number, and it will print out the data in that column (in sentences or in a chart,
# for however many items remain).
# - You can sort the list according to any of the remaining columns in ascending or descending order.
# - There are functions to reset the results list and to only print the list.
# - There is a function that runs a multiple-choice trivia quiz, which loops and keeps track of score until you exit it.
# - Finally, there is a function for finding a singular value, which aligns best with the original requirements

# IMPROVEMENTS/MODIFICATIONS:
# 1 - The data includes all 256 countries and territories rather than just the top 25,
# as well as the area, average life expectancy, and death rate of the countries, in addition to the requirements.
# 2 - You don't have to type in the exact name of the country to find it, but rather any substring that it may contain
# As such, it can return multiple countries in a list rather than just one
# 3 - Searching rows and columns are separated to allow for greater search control, so you can narrow down results
# first before cutting out all possible answers. They can be done iteratively, for example you can search for
# "united", then "united arab emirates" then "2" to find the GDP of the United Arab Emirates.
# 4 - There is a sorting function, which can sort all remaining results in ascending or descending order, depending on
# any of the remaining columns in the results list. Blank values are pushed to the end for both orders.
# 5 - A trivia game was incorporated, which asks the user multiple choice questions about x stat for x country,
# and keeps track of the score (x questions out of y correct).
# - Error handling was incorporated, as always

# The library tabulate was used - https://pypi.org/project/tabulate/

# ************************************************************************

from tabulate import tabulate

import random

import copy
# Set up CSV
import csv

data_list = open('data.csv', 'r')
reader = csv.reader(data_list)
# Creating the main list of countries
countries = []
for row in reader:
    countries.append(row)
# Creating a list of names of columns
columns = []
for col in countries[0]:
    columns.append(col)
# Delete the first row, which contains the names of columns from main list
del countries[0]
# Convert GDP to billions and unemployment to percent
for row in countries:
    try:  # GDP
        row[2] = str(float(row[2].replace(',', '')) / 1000000000) + " billion"
    except ValueError:
        pass
    try:  # Unemployment
        row[3] = str(float(row[3].replace(',', ''))) + "%"
    except ValueError:
        pass


# Returns inputted string that is alphabetical (except spaces and commas)
def getSearchedString():
    search = input("Enter a string to search for: ")
    while not search.replace(' ', '').replace(',', '').isalpha():  # Input should not have numbers or punctuation
        search = input("Invalid input - Please enter only letters: ")
    return search


# Return inputted number that corresponds with a column in the data
def getColumn():
    # Legend for column numbers
    print("COLUMNS:", sep="")
    for a in range(len(columns)):
        print(a, ": ", columns[a], sep='')
    print("(Enter 0 only if you are using the sorting function)\n")
    # Get input
    while True:
        try:
            search = int(input("Enter a column number (reference COLUMNS legend above): "))
            if 0 <= search <= len(columns) - 1:  # Must be within range
                return search
            print("Invalid input - Number not in range")
        except ValueError:  # Must be a number
            print("Invalid input - Input must be a number")


# Searches list of countries for rows containing the string, returns list of matching countries
def narrowDownCountries(searchedValue, data):
    found = []
    for n in data:  # Match countries and add them to list 'found'
        if not n[0].lower().find(searchedValue.lower()) == -1:
            found.append(n)
    return found


# Removes all data columns in the list other than the country name and specified column
def narrowDownColumn(column_, data):
    for row_ in data:  # Loop through all items
        for a in range(len(row_) - 1, 0, -1):  # Delete all indices other than the one specified
            if a != column_:
                del row_[a]
    return data


# Sorts the data using selection sort, by a specified column and order.
def sortByColumn(c, order, data):
    print("\nSorting by", columns[c], "in", "descending" if order == 1 else "ascending", "order...")
    # Loop to successively reduce unsorted subarray by increasing sorted section on the left
    for n in range(len(data)):
        keyIndex = n  # Index that will be compared to and switched with m (below) for each sorting iteration
        for m in range(n + 1, len(data)):
            if c != 0:  # Sort by numbers, the below converts strings to numbers
                try:  # order = 1 is for max index, order = 2 is for min index
                    if (order == 1 and float(''.join(a for a in data[keyIndex][c] if a.isdigit() or a == '.'))
                        < float(''.join(a for a in data[m][c] if a.isdigit() or a == '.'))) or \
                            (order == 2 and float(''.join(a for a in data[keyIndex][c] if a.isdigit() or a == '.'))
                             > float(''.join(a for a in data[m][c] if a.isdigit() or a == '.'))):
                        keyIndex = m
                except ValueError:
                    if data[keyIndex][c] == '':
                        keyIndex = m
            else:  # Easier to find key index if sorted by name
                if order == 1 and data[keyIndex][c] < data[m][c] or order == 2 and data[keyIndex][c] > data[m][c]:
                    keyIndex = m
        data[n], data[keyIndex] = data[keyIndex], data[n]  # Switch in the correct value to add to the sorted section
    return data  # Return sorted list


# Runs a loop trivia quiz that generates multiple choice questions and keeps track of score
def trivia():
    print("-" * 100, "\nStart quiz")
    score = [0, 0]
    while True:
        # Generate question
        country = random.randint(0, len(countries) - 1)  # Country
        col_ = random.randint(1, len(columns) - 1)  # Row
        ans = random.randint(1, 4)  # Spot of correct option
        while countries[country][col_] == '':  # Ensure they are
            country = random.randint(0, len(countries) - 1)
            col_ = random.randint(0, len(columns) - 1)
        # Print question
        print("What is the", columns[col_], "of", countries[country][0], "?")
        for b in range(1, 5):  # Options
            if b == ans:  # Insert correct option
                print(chr(b + 64), "-", countries[country][col_])
            else:  # Other options
                nr = random.randint(0, len(countries)-1)
                while countries[nr][col_] == '':
                    nr = random.randint(0, len(countries) - 1)
                print(chr(b + 64), "-", countries[nr][col_])
        print()
        # Get a integer
        while True:
            g = input("Enter an option: ").upper()
            if g in ["A", "B", "C", "D"] and g != "":
                g = ord(g) - 64
            else:
                print("Invalid input - Please enter A, B, C, or D")
                continue
            if 0 <= g <= 4:
                break
        print()
        score[1] += 1
        if g == ans:
            print("That is correct!")
            score[0] += 1
        else:
            print("Incorrect - the correct answer is", chr(ans + 64), "-", countries[country][col_])
        print("\nYour current score is:", score[0], "/", score[1])
        # Quit or continue based on user input
        if input("\nEnter anything to quit, Enter nothing to continue: ") != "":
            print()
            break
        print()


def basicProcedure():
    while True:  # Enter a searched string until the searched string is valid
        stringSearched = getSearchedString()
        temp = narrowDownCountries(stringSearched, countries)
        if 1 <= len(temp) <= 9:
            print()
            break
        elif len(temp) == 0:
            print("\nNo results found - Try again\n")
        elif len(temp) >= 10:
            print("\nSearched string is too short or too general - Try again\n")
    # Print out the options
    print("Results:")
    for u in range(len(temp)):
        print(u + 1, "-", temp[u][0])
    print()
    # Get the user to choose one of the options
    while True:
        try:
            choice = int(input("Choose one of the countries above by entering a number: "))
            if 1 <= choice <= len(temp):
                break
            else:
                print("Invalid input - Enter one of the values above")
        except ValueError:
            print("Invalid input - Please enter a number")
    temp = narrowDownCountries(temp[choice - 1][0], temp)  # Narrow down temp to the chosen country
    print("\n", temp[0][0], "\n", sep='')
    # Get column and then narrow down temp to just that column
    column_ = getColumn()
    narrowDownColumn(column_, temp)
    print()
    printResults(column_, temp)  # Print result as a sentence
    print()


# Prints a sentence for 2d list with two columns
def printResults(column, data):
    try:
        for row_ in data:
            print("The", columns[column], "of", row_[0], "is", row_[1] if row_[1] != "" else "unavailable")
    except IndexError:
        print("Error: Only one column remains in the data list - Please reset the results list")


# Print out the full data and the instructions
print(tabulate(countries, headers=columns, showindex=(idx + 1 for idx in range(len(countries))), tablefmt="mixed_grid"))
print("\n", "-" * 100, "\n\nThis program searches a file containing 256 countries & territories with data regarding:",
      sep='')
for i in range(1, len(columns)):
    print(i, ": ", columns[i], sep='')
print("\nFEATURES:\nYou can search the list of countries by entering a string, and the program will produce a chart/"
      "list of countries with names that contain the string\nYou can also enter a column number, and it will "
      "print out the data for that column (in sentences or with a chart, for however many items)\nThese can be done "
      "iteratively, for example you can search for 'united', then 'united arab emirates' then '2' to find the GDP of "
      "the United Arab Emirates\nYou can also sort the list according to any of the remaining columns in ascending or "
      "descending order\nThere is a function that runs a multiple-choice trivia quiz, which loops and keeps track of "
      "score until you exit it\nFinally, there is a function for finding a singular value, which aligns best with the "
      "original requirements\n", sep='')

col = 0

results = copy.deepcopy(countries)  # Copy of the original list

# Loop for iterative searching (you can search the results of a search and so on)
while True:
    input("press enter to continue... ")
    print("\n", "-" * 100, "\n", sep='')

    # Actions chosen by input x (with error handling)
    x = input("Enter 1 to search countries (rows) by string\nEnter 2 to find a column\nEnter 3 to sort by "
              "column\nEnter 4 to reset results list\nEnter 5 to only print list\nEnter 6 for a trivia quiz\nEnter 7 "
              "for the basic procedure (search countries and then select column)\nEnter 0 to quit\n\nSelect action: ")
    while x not in ["0", "1", "2", "3", "4", "5", "6", "7"]:
        x = input("Invalid input - Please enter one of the options above: ")
    print()

    if x == "1":  # Search for country
        substring = getSearchedString()  # Get input string
        results = narrowDownCountries(substring, results)  # Search
    elif x == "2":  # Narrow down column
        if len(results[0]) <= 2:
            print("Error - Please reset the results list before running this action\n")
            continue
        # Processing
        col = getColumn()  # Get column
        results = narrowDownColumn(col, results)  # Delete everything else
    elif x == "3":  # Sort list
        if len(results[0]) == 2:  # If there are only two columns left
            print("This list can be sorted by", columns[col], "or name - Reset the list to sort by another parameter")
            sortedCol = input("Enter 1 to sort by " + columns[col] + ", Enter 0 to sort by country name: ")
            while sortedCol not in ["0", "1"]:
                sortedCol = input("Invalid input - Enter 1 or 0: ")
            sortedCol = int(sortedCol)
        elif len(results[0]) == 1:  # If there is only 1 column left
            print("This list can only be sorted by country name\n")
            sortedCol = 0
        else:  # If there is a full list
            sortedCol = getColumn()
        # Input for whether it is descending or ascending order
        o = input("\nEnter 1 for descending order and 2 for ascending order: ")
        while o not in ["1", "2"]:
            o = input("Invalid input - Try again: ")
        o = int(o)
        # Sort
        results = sortByColumn(sortedCol, o, results)
    elif x == "4":  # Reset results list
        results = copy.deepcopy(countries)
        print("The list has been reset to the original\n")
        continue
    elif x == "6":  # Trivia
        trivia()
        continue
    elif x == "7":  # Standard procedure that only results in one value
        print("This will search the whole list, not the temporary results\n")
        basicProcedure()
        continue
    elif x == "0":  # Exit
        exit()
    # Just printing the list does not require any procedure

    # Print the current results
    print("\nCurrent Results:")
    try:
        if len(results[0]) == 2:  # Use function if columns have already been narrowed down
            print("Two columns remaining - ", end='')
            if input("Print results in sentences or a table? (1 for sentences, anything else for a table): ") == '1':
                print()
                printResults(col, results)
            else:
                print(tabulate(results, headers=["country", columns[col]],
                               showindex=(idx + 1 for idx in range(len(results))), tablefmt="mixed_grid"))
        else:  # Otherwise just print it
            print(tabulate(results, headers=columns, showindex=(idx + 1 for idx in range(len(results))),
                           tablefmt="mixed_grid"))
    # Reset list of there are no results
    except IndexError:
        print("None, resetting list...")
        results = copy.deepcopy(countries)
    print()
