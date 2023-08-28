import csv

def process_c3_value(value):
    if "居民会" in value:
        return value.replace("居民会", "")
    elif "村村" in value:
        return value.replace("村村", "村")
    return value

input_file = "area_code.csv"

# Create a temporary list to store the updated data
updated_data = []

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row["c2"] = process_c3_value(row["c2"])
        updated_data.append(row)

# Write the updated data back to the original file
with open(input_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["c1", "c2", "c3", "c4"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_data)

print("Column 'c3' in the CSV file has been updated.")
