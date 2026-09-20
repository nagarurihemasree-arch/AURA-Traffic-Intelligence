import pandas as pd


def count_similar_complaints(category, location):
    # Load previous city complaints
    data = pd.read_csv("data/city_complaints.csv")

    # Find complaints with the same category AND location
    similar = data[
        (data["category"] == category) &
        (data["location"] == location)
    ]

    # Count how many similar complaints were found
    complaint_count = len(similar)

    return complaint_count


# Testing the function
if __name__ == "__main__":

    category = "Water Leakage"
    location = "Area A"

    count = count_similar_complaints(category, location)

    print("\n--- SIMILAR COMPLAINT ANALYSIS ---")

    print(f"\nCategory: {category}")
    print(f"Location: {location}")

    print(f"\nSimilar Complaints Found: {count}")