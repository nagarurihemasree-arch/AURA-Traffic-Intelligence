import pandas as pd

# Load the complaint dataset
data = pd.read_csv("data/complaints.csv")

# Show all the data
print(data)

# Show total number of complaints
print("\nTotal complaints:", len(data))

# Show all available categories
print("\nCategories:")
print(data["category"].unique())