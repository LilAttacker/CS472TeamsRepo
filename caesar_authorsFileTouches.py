import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttokens, ct):
    jsonData = None
    try:
        ct = ct % len(lsttokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttokens[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(f"Error: {e}")
    return jsonData, ct

# Function to get the commit history for a specific file
def get_commit_history_for_file(filename, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    authors_dates = []

    try:
        while True:
            spage = str(ipage)
            # API to get commits for a specific file
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?path={filename}&page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # Break out of the while loop if there are no more commits
            if len(jsonCommits) == 0:
                break

            # Iterate through each commit
            for commit in jsonCommits:
                author = commit['commit']['author']['name']
                date = commit['commit']['author']['date']
                authors_dates.append((filename, author, date))
            
            ipage += 1

    except Exception as e:
        print(f"Error retrieving data for file {filename}: {e}")
    
    return authors_dates

# Read the list of files from the previous output
def get_file_list_from_csv(fileOutput):
    file_list = []
    with open(fileOutput, mode='r') as fileCSV:
        reader = csv.reader(fileCSV)
        next(reader)  # Skip header
        for row in reader:
            file_list.append(row[0])  # Filename is in the first column
    return file_list

# Main function to collect authors and dates for each file
def collect_authors_dates(dictfiles, lsttokens, repo, fileOutput):
    file_list = get_file_list_from_csv(fileOutput)
    results = []

    for filename in file_list:
        print(f"Processing file: {filename}")
        file_commit_history = get_commit_history_for_file(filename, lsttokens, repo)
        results.extend(file_commit_history)

    return results

# GitHub repo
repo = 'scottyab/rootbeer'

# put your tokens here
lstTokens = ["fake_token1", "fake_token2", "fake_token3"]

# Read the previous output CSV file to get the list of source files
fileOutput = 'data/file_sourcerootbeer.csv'

# Collect authors and dates for each file in the list
results = collect_authors_dates({}, lstTokens, repo, fileOutput)

# Write the results to a new CSV file
output_csv = 'data/authors_dates_rootbeer.csv'
with open(output_csv, mode='w') as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(["Filename", "Author", "Date"])  # Header

    for result in results:
        writer.writerow(result)

print(f"Author and date information written to {output_csv}")
