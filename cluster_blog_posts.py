import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load data
df = pd.read_excel("thalamus_blog_content.xlsx")

# Convert published_date to datetime (optional, but recommended)
df["published_date"] = pd.to_datetime(df["published_date"])

# Fill NaN content with empty string
texts = df["content"].fillna("")

# Vectorize text with TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(texts)

# Number of clusters (adjust as needed)
num_clusters = 3

# KMeans clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)

# Add cluster labels to dataframe
df["cluster"] = kmeans.labels_

# Get the feature names (words)
terms = vectorizer.get_feature_names_out()

print(f"Top terms per cluster:")

order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

for i in range(num_clusters):
    print(f"\nCluster {i}:")
    top_terms = [terms[ind] for ind in order_centroids[i, :10]]
    print(", ".join(top_terms))

# Save the dataframe with clusters
df.to_excel("thalamus_blog_content_with_clusters.xlsx", index=False)

print("\n✅ Clustering complete. Results saved to 'thalamus_blog_content_with_clusters.xlsx'.")
