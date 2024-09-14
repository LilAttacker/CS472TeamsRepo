from __future__ import annotations
from collections import defaultdict
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


REPO = "rootbeer"
INPUT_FILE_NAME = f"data/touches_{REPO}.csv"
OUTPUT_FILE_NAME = f"data/scatterplot_{REPO}.png"


def get_weeks(initial: datetime, current: datetime) -> int:
    """Returns the number of weeks from the initial date to the current 
    date."""
    difference = current - initial
    return difference.days // 7


def to_datetime(date_str: str) -> datetime:
    """Converts to a datetime object."""
    if date_str.endswith("Z"):
        date_str = date_str[:-1]
    return datetime.fromisoformat(date_str)

def main() -> None:
    """Main entry point function."""

    print("Running...")

    # Read information from file
    touches: list[dict]
    with open(INPUT_FILE_NAME) as input_file:
        reader = csv.DictReader(input_file)
        touches = list(reader)

    # Weeks calculation
    for touch in touches:
        touch["Date"] = to_datetime(touch["Date"])
    touches.sort(key=lambda t: t["Date"])
    initial_date: datetime = touches[0]["Date"]
    for touch in touches:
        touch["weeks"] = get_weeks(initial_date, touch["Date"])

    # File calculation
    file_names = sorted(set(t["Filename"] for t in touches))
    file_names_to_indices = {fn: i for i, fn in enumerate(file_names)}

    for touch in touches:
        touch["file"] = file_names_to_indices[touch["Filename"]]

    # Collect authors
    authors_to_touches = defaultdict(list)
    for touch in touches:
        authors_to_touches[touch["Author"]].append(touch)

    # Plot the points
    plt.figure(figsize=(10, 5))
    
    for author, touches in authors_to_touches.items():
        x = []
        y = []
        for touch in touches:
            x.append(touch["file"])
            y.append(touch["weeks"])
        plt.scatter(x, y, label=author)
    
    plt.legend(loc=(1.05, 0.0))
    plt.tight_layout(pad=1.5)
    plt.xlabel("file")
    plt.ylabel("weeks")
    plt.xticks(np.arange(0, len(file_names), step=1), minor=True)
    plt.savefig(OUTPUT_FILE_NAME)

    print("File File_name")
    for i, file_name in enumerate(file_names):
        print(f"{i:>4} {file_name}")
    print(f"Plotted contribution data to: {OUTPUT_FILE_NAME}")



if __name__ == "__main__":
    main()
