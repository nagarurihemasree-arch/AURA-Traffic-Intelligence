import csv
from datetime import datetime, timedelta


input_file = "data/city_complaints.csv"


# Read all rows
with open(input_file, "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)


# Start date for our prototype data
start_date = datetime(2026, 8, 28)


updated_rows = []

# Add correct header
updated_rows.append(["text", "category", "location", "date"])


# Process complaint rows
for i, row in enumerate(rows[1:]):

    # Remove an empty date column if it exists
    row = row[:3]

    # Create a date
    complaint_date = start_date + timedelta(days=i % 8)

    date_string = complaint_date.strftime("%Y-%m-%d")

    # Add the date
    updated_rows.append(row + [date_string])


# Save updated CSV
with open(input_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(updated_rows)


print("✅ Dates added successfully!")

print("\nFirst 5 rows:")
for row in updated_rows[:6]:
    print(row)