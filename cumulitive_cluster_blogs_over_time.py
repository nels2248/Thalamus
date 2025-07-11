import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# 1. Load data
df = pd.read_excel("thalamus_blog_content.xlsx")

# 2. Convert published_date to datetime
df["published_date"] = pd.to_datetime(df["published_date"])

# 3. Vectorize text with TF-IDF
texts = df["content"].fillna("")
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X = vectorizer.fit_transform(texts)

# 4. Cluster with KMeans
num_clusters = 5  # adjust as needed
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)
df["cluster"] = kmeans.labels_

# 5. Generate cluster names from top keywords
terms = vectorizer.get_feature_names_out()
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
num_top_words = 5

cluster_names = {}
for i in range(num_clusters):
    top_words = [terms[ind] for ind in order_centroids[i, :num_top_words]]
    cluster_names[i] = ", ".join(top_words)

print("Cluster names:")
for cid, name in cluster_names.items():
    print(f"  Cluster {cid}: {name}")

# 6. Prepare data for cumulative plot
df["year_month"] = df["published_date"].dt.to_period("M")

counts = (
    df.groupby(["cluster", "year_month"])
    .size()
    .reset_index(name="post_count")
)

# Fill missing months with zeros for each cluster
all_months = pd.period_range(df["year_month"].min(), df["year_month"].max(), freq="M")
clusters = counts["cluster"].unique()
index = pd.MultiIndex.from_product([clusters, all_months], names=["cluster", "year_month"])

counts = counts.set_index(["cluster", "year_month"]).reindex(index, fill_value=0).reset_index()
counts = counts.sort_values(["cluster", "year_month"])

# Calculate cumulative sums per cluster
counts["cumulative_posts"] = counts.groupby("cluster")["post_count"].cumsum()

# 7. Plot cumulative lines per cluster
plt.figure(figsize=(12, 7))

# Grab one group's x-axis to control tick spacing
sample_x = sorted(counts["year_month"].astype(str).unique())
tick_indices = [i for i in range(0, len(sample_x), max(1, len(sample_x)//6))]
tick_labels = [sample_x[i] for i in tick_indices]

for cluster_id, group in counts.groupby("cluster"):
    label = cluster_names.get(cluster_id, f"Cluster {cluster_id}")
    plt.plot(
        group["year_month"].astype(str),
        group["cumulative_posts"],
        marker="o",
        label=label,
    )

plt.xlabel("Month")
plt.ylabel("Cumulative Number of Posts")
plt.title("Cumulative Blog Posts Over Time by Cluster")
plt.xticks(tick_indices, tick_labels, rotation=45)
plt.grid(True)
plt.legend(title="Clusters")
plt.tight_layout()

chart_file = "cumulative_blog_posts_by_cluster.png"
plt.savefig(chart_file)
plt.close()

# 8. Generate simple HTML embedding the plot image
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Cumulative Blog Posts by Cluster</title>
</head>
<body>
    <h1>Cumulative Blog Posts Over Time by Cluster</h1>
    <img src="{chart_file}" alt="Cumulative Blog Posts by Cluster" style="max-width:100%; height:auto;">
</body>
</html>
"""

html_file = "cumulative_blog_posts_by_cluster.html"
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\n✅ Clustering and cumulative plot complete.")
print(f"   - Chart image saved as '{chart_file}'")
print(f"   - HTML file saved as '{html_file}'")
