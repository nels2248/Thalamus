import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS


# 1. Load data
df = pd.read_excel("thalamus_blog_content.xlsx")

# 2. Convert published_date to datetime
df["published_date"] = pd.to_datetime(df["published_date"])

# 3. Vectorize text
# Combine default English stop words with your custom ones
custom_stop_words = list(ENGLISH_STOP_WORDS.union({'thalamus'}))
texts = df["content"].fillna("")
vectorizer = TfidfVectorizer(stop_words=custom_stop_words, max_features=1000)
X = vectorizer.fit_transform(texts)

# 4. Cluster with KMeans
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X)
df["cluster"] = kmeans.labels_

# 5. Get cluster names from top keywords
terms = vectorizer.get_feature_names_out()
order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
cluster_names = {}
for i in range(num_clusters):
    top_words = [terms[ind] for ind in order_centroids[i, :2]]
    cluster_names[i] = ", ".join(top_words)

# 6. Assign year-month
df["year_month"] = df["published_date"].dt.to_period("M")

# 7. Count posts per month per cluster
counts = df.groupby(["year_month", "cluster"]).size().reset_index(name="post_count")

# 8. Create full month range
all_months = pd.period_range(df["year_month"].min(), df["year_month"].max(), freq="M")
month_df = pd.DataFrame({"year_month": all_months})

# 9. Build cumulative total per month and track clusters
cumulative = []
running_total = 0

# For each month, find the dominant cluster and increment cumulative count
for ym in all_months:
    month_data = counts[counts["year_month"] == ym]
    total_posts = month_data["post_count"].sum()
    if not month_data.empty:
        # Take cluster with the most posts that month
        dominant_cluster = month_data.sort_values("post_count", ascending=False).iloc[0]["cluster"]
    else:
        dominant_cluster = np.nan  # No posts this month
    running_total += total_posts
    cumulative.append((ym.to_timestamp(), running_total, dominant_cluster))

cum_df = pd.DataFrame(cumulative, columns=["date", "cumulative_count", "cluster"])

# 10. Plot single line with color segments by cluster
plt.figure(figsize=(12, 7))

# Define a color map for clusters
colors = plt.get_cmap("tab10").colors
cluster_color_map = {cid: colors[i % len(colors)] for i, cid in enumerate(cluster_names)}

# Draw color-coded line segments
for i in range(1, len(cum_df)):
    c1 = cum_df.iloc[i - 1]
    c2 = cum_df.iloc[i]
    cluster = c2["cluster"]
    color = cluster_color_map.get(cluster, "gray")
    plt.plot(
        [c1["date"], c2["date"]],
        [c1["cumulative_count"], c2["cumulative_count"]],
        color=color,
        linewidth=2
    )

# Format plot
plt.xlabel("Date")
plt.ylabel("Cumulative Blog Posts")
plt.title("Cumulative Blog Posts with Color-Coded Clusters")

# Set clean x-axis ticks (6 total)
tick_indices = np.linspace(0, len(cum_df) - 1, 6, dtype=int)
tick_labels = [cum_df.iloc[i]["date"].strftime("%b %Y") for i in tick_indices]
tick_positions = [cum_df.iloc[i]["date"] for i in tick_indices]
plt.xticks(tick_positions, tick_labels, rotation=45)

# Legend with cluster names
legend_items = [
    Line2D([0], [0], color=cluster_color_map[cid], lw=3, label=cluster_names[cid])
    for cid in cluster_names
]
plt.legend(handles=legend_items, title="Cluster Topics")

plt.grid(True)
plt.tight_layout()

# Save chart and HTML
chart_file = "single_colored_cumulative_line.png"
plt.savefig(chart_file)
plt.close()

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cumulative Blog Timeline by Cluster</title>
</head>
<body>
    <h1>Cumulative Blog Posts Over Time</h1>
    <p><strong>Color segments represent different content clusters.</strong></p>
    <img src="{chart_file}" alt="Cumulative Blog Line with Clusters" style="max-width:100%; height:auto;">
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\n✅ Created single-line cumulative chart with color-coded clusters.")
print(f"   - Chart image saved as '{chart_file}'")
print(f"   - HTML file saved as 'single_colored_cumulative_line.html'")
