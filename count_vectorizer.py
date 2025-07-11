import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# Load the blog content Excel file
df = pd.read_excel("thalamus_blog_content.xlsx")

# Initialize CountVectorizer with stop words and max features
vectorizer = CountVectorizer(stop_words="english", max_features=20)

# Fit and transform the 'content' column (fill NaNs with empty strings)
X = vectorizer.fit_transform(df["content"].fillna(""))

# Get feature names (top keywords)
keywords = vectorizer.get_feature_names_out()

# Sum the counts of each keyword across all documents
counts = X.toarray().sum(axis=0)

print("Keyword frequencies:")
for kw, count in zip(keywords, counts):
    print(f"{kw}: {count}")
