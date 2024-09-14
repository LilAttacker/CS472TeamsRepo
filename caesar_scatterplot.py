import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Function to convert the date to the number of weeks since the start of the project
def weeks_since_start(date_str, start_date):
    commit_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    delta = commit_date - start_date
    return delta.days // 7

# Load the data from CSV
def load_data(csv_file):
    data = []
    with open(csv_file, 'r') as fileCSV:
        reader = csv.DictReader(fileCSV)
        for row in reader:
            data.append(row)
    return data

# Main function to generate the scatter plot
def plot_scatter(data, output_file):
    # Extract unique authors
    authors = list({row['Author'] for row in data})
    author_colors = {author: i for i, author in enumerate(authors)}
    cmap = plt.get_cmap('tab20', len(authors))  # Use a distinct colormap with 20 distinct colors

    # Extract unique file names and assign them numbers for the x-axis
    file_names = list({row['Filename'] for row in data})
    file_numbers = {filename: i + 1 for i, filename in enumerate(file_names)}  # Map file name to file number

    # Convert dates to weeks since the start of the project
    all_dates = [datetime.strptime(row['Date'], "%Y-%m-%dT%H:%M:%SZ") for row in data]
    start_date = min(all_dates)  # The earliest commit date marks the start of the project
    
    weeks_list, file_nums, color_indices = [], [], []

    for row in data:
        filename = row['Filename']
        author = row['Author']
        date = row['Date']

        # Compute the number of weeks since the start of the project
        weeks = weeks_since_start(date, start_date)
        weeks_list.append(weeks)

        # Get the corresponding file number
        file_num = file_numbers[filename]
        file_nums.append(file_num)

        # Map the author to a color index (numerical)
        color_indices.append(author_colors[author])

    # Create scatter plot
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(file_nums, weeks_list, c=color_indices, cmap=cmap, alpha=0.8, edgecolor='k')

    # Create a legend for the authors
    unique_authors = list(author_colors.keys())
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(author_colors[author]), markersize=8, label=author) for author in unique_authors]
    plt.legend(handles=handles, title="Authors", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Label the axes
    plt.xlabel('File Number (representing different files)')
    plt.ylabel('Weeks since project start')
    plt.title('File Touches Over Time by Author')

    # Save plot as PNG file
    plt.tight_layout()
    plt.savefig(output_file, format='png')
    plt.close()

# File containing the authors and dates data
csv_file = 'data/authors_dates_rootbeer.csv'

# Load data
data = load_data(csv_file)

# Output file name for the plot
output_file = 'data/scatter_plot_by_file.png'

# Plot scatter plot and save it as a PNG
plot_scatter(data, output_file)

print(f"Scatter plot saved as {output_file}")
