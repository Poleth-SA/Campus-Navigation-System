import csv

with open("data/campus.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)  # Check if rows are read correctly