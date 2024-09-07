import json
import requests
import csv
import git
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os

if not os.path.exists("data"):
    os.makedirs("data")



# Lists to track info gathered from authorsFileTouches
authorList = []
weeklyList = []
sourceList = []
# Retrieves all info from authorsFileTouches's output
def retrieveAuthorInfo():
    with open(fileInput1, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                authorList.append(row["AuthorsHelped"])
                weeklyList.append(row["DateOfPosting"])
                sourceList.append(row["FileModified"])
                line_count += 1
    return



# Auth Token
lstTokens = [""]

# Open file with output from collecting author and date of commits
repo = 'scottyab/rootbeer'
file = repo.split('/')[1]
fileInput1 = 'data/authors_' + file + '.csv'
retrieveAuthorInfo()


# Gathers the date of the first commit and converts it to a datetime object
# The last object in the list is the oldest commit
endDatestr = weeklyList[-1]
end_date = datetime.datetime.strptime(endDatestr, '%Y-%m-%d')

# Loops through every date gathered earlier and turns them into weeks based
# on how many days later they are from the starting date confirmed earlier
for week_id, currentWeek in enumerate(weeklyList):
    current_Date = datetime.datetime.strptime(currentWeek, '%Y-%m-%d')
    lengthInDays = current_Date - end_date
    # Needed to convert the datetime  object into just the days
    day_num = lengthInDays.days
    # Converts the days into weeks
    week_num = day_num//7
    # Overwrites the previous date number to just a week number
    weeklyList[week_id] = week_num


# Loops through the source file list and converts each instance of a file found into
# a single number mask. This is for the scatter plot, so it doesn't get messy.
fileMask = 0
for source_id, currentFile in enumerate(sourceList):
    if not isinstance(currentFile, int):
        fileName = currentFile
        # Have to loop through the list for each instance of the file name
        for newSource_id, replaceFile in enumerate(sourceList):
            if replaceFile == fileName:
                sourceList[newSource_id] = fileMask
        fileMask += 1


# Loops through the name list of the authors and converts each to a singular number
# This number is to track their color so contributions can be better determined
nameMask = 0
for name_id, currentName in enumerate(authorList):
    if not isinstance(currentName, int):
        authorName = currentName
        for newName_id, replaceName in enumerate(authorList):
            if replaceName == authorName:
                authorList[newName_id] = nameMask
        nameMask += 1


# Reverses the lists of each so the oldest is the first rather than last
weeklyList.reverse()
authorList.reverse()
sourceList.reverse()


# Plots the scatterplot using the masked files list and weeks found earlier.
# The color of each plot is based on the authors number.
plt.scatter(sourceList, weeklyList, c=authorList, s=50, cmap='tab20') # s is a size of marker 
plt.yscale('linear')
plt.xlabel('File')
plt.ylabel('Weeks')