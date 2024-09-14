from __future__ import annotations
import csv
import os
import requests

try:
    GITHUB_MINE_TOKEN = os.environ["GITHUB_MINE_TOKEN"]
except KeyError:
    print("Error: No environment token specified for GITHUB_MINE_TOKEN")
    print("  Either set it, or replace it in code with the correct token.")
    exit(1)

OWNER = "scottyab"
REPO = "rootbeer"

INPUT_FILE_NAME = f"data/file_{REPO}.csv"
OUTPUT_FILE_NAME = f"data/touches_{REPO}.csv"

def request_file_commit_list(owner: str, repo: str, file_path: str) -> list:
    """Requests the commits for the given file in the specified repository."""
    response = requests.get(
        url=f"https://api.github.com/repos/{owner}/{repo}/commits",
        headers={
            "Authorization": f"Bearer {GITHUB_MINE_TOKEN}",
        },
        params={
            "path": file_path,
        },
    )
    # print(response.text)
    return response.json()


def main() -> None:
    """Main entry point function."""

    print("Running...")
    
    # Collect input infos (Filename, Touches) from input file
    print(f"Reading from: {INPUT_FILE_NAME}")
    input_infos: list[dict]
    with open(INPUT_FILE_NAME) as input_file:
        reader = csv.DictReader(input_file)
        input_infos = list(reader)

    # Request info about commits for the files
    file_names_to_file_commit_lists: dict[str, list] = {}
    for input_info in input_infos:
        file_name = input_info["Filename"]
        file_names_to_file_commit_lists[file_name] = request_file_commit_list(
            OWNER, REPO, file_name
        )
        print(f"Requested commits for: {file_name}")

    # Compile information about Filename, CommitSHA, Author, and Date
    touch_infos: list[dict] = []
    for file_name, file_commit_list in file_names_to_file_commit_lists.items():
        for file_commit in file_commit_list:
            touch_infos.append(
                {
                    "Filename": file_name,
                    "CommitSHA": file_commit["sha"],
                    "Author": file_commit["commit"]["author"]["name"],
                    "Date": file_commit["commit"]["author"]["date"],
                }
            )
    touch_infos.sort(key=lambda info: info["Date"])

    # Write info to file
    with open(OUTPUT_FILE_NAME, "w") as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=["Filename", "CommitSHA", "Author", "Date"],
        )
        writer.writeheader()
        for touch_info in touch_infos:
            writer.writerow(touch_info)
    print(f"Done. Wrote to {OUTPUT_FILE_NAME}")


if __name__ == "__main__":
    main()
