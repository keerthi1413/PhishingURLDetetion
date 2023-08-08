import csv

# Read the CSV file
with open('feed.csv', 'r') as file:
    reader = csv.reader(file)
    url_list = list(reader)

# Get user input for the URL to search
search_url = input("Enter the URL to search: ")

# Iterate through the URL list and search for the URL
found = False
for row in url_list:
    if search_url in row:
        print("URL found: ", row[0])
        found = True
        break

# If URL not found in the list, print message
if not found:
    print("URL not found in the dataset.")
