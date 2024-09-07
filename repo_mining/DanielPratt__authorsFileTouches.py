import json
import requests
import csv
import git

import os

if not os.path.exists("data"):
 os.makedirs("data")


sourceList = []
# Takes in the output from CollectFiles and records all file names
# that are apart of the source list
def listSourceFiles():
    with open(fileInput, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            sourceList.append(row["Filename"])
            line_count += 1
    return



# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct



# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(fileNameURL, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']

                # Grabs each filename in every commit
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename in sourceList:
                        # So long as that file is apart of our source files, then
                        # we save the contents URL as that is the commit number
                        contentsURL = filenameObj['contents_url']
                        commitNumbers.append(contentsURL[-40:])

                        # If its the first file for that we have to initialize
                        # it as a list for the dict. Otherwise we append to the list
                        if contentsURL[-40:] in fileNameURL:
                            fileNameURL[contentsURL[-40:]].append(filename)
                        else:
                            fileNameURL[contentsURL[-40:]] = []
                            fileNameURL[contentsURL[-40:]].append(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)


# Auth token
lstTokens = [""]

# Open file with output from collecting source files
repo = 'scottyab/rootbeer'
file = repo.split('/')[1]
fileInput = 'data/file_' + file + '.csv'
listSourceFiles()

# Collect Authors / Dates of commits to files found in collectfiles.py
commitNumbers = []
fileNameURL = dict()
countfiles(fileNameURL, lstTokens, repo)

# Creates new output file
fileOutput = 'data/authors_' + file + '.csv'
fileOutputTxt = open(fileOutput, 'w')
fileOutputTxt.write("AuthorsHelped,DateOfPosting,FileModified")

# Initialize a Git repository object
repoCommits = git.Repo("/Users/Danie/AppData/Local/Programs/Microsoft VS Code/rootbeer")


fileList = []
# Iterate over each commit
for commit in repoCommits.iter_commits():
    commitString = str(commit)

    # So long as the commit matches a string found in the files from before, then we see
    # who published that commit and when
    if commitString in commitNumbers:
        author = commit.author.name
        date = commit.committed_datetime.strftime('%Y-%m-%d')
        fileList = fileNameURL[commitString]
        # Have to loop through all associated file names with that commit
        # otherwise, it'll only track one file per commit, even if multiple files were
        # impacted
        for fileCommitted in fileList:
            fileOutputTxt.write(f"\n{author},{date},{fileCommitted}")

# Close output file
fileOutputTxt.close()