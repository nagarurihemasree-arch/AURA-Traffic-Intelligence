import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the cleaned dataset
data = pd.read_csv("data/cleaned_complaints.csv")

# Get the cleaned complaint text
texts = data["cleaned_text"]

# Create the TF-IDF machine
vectorizer = TfidfVectorizer()

# Learn the words and convert text into numbers
X = vectorizer.fit_transform(texts)

# Show all the words learned by TF-IDF
print("Words learned by TF-IDF:")
print(vectorizer.get_feature_names_out())

# Show the size of our numerical data
print("\nTF-IDF Matrix Shape:")
print(X.shape)
# Convert TF-IDF matrix into a table
tfidf_dataframe = pd.DataFrame(
    X.toarray(),
    columns=vectorizer.get_feature_names_out()
)

# Show the TF-IDF values
print("\nTF-IDF Numbers:")
print(tfidf_dataframe)
print("\nFirst Complaint:")
print(data["cleaned_text"].iloc[0])

print("\nTF-IDF Numbers for First Complaint:")
print(tfidf_dataframe.iloc[0])
# Get the correct categories
y = data["category"]

print("\nCategories (Correct Answers):")
print(y)

print("\nNumber of complaints:")
print(len(y))