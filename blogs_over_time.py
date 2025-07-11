import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("thalamus_blog_content.xlsx")

# Convert published_date to datetime
df["published_date"] = pd.to_datetime(df["published_date"])

# Group by Year-Month and count posts
df["year_month"] = df["published_date"].dt.to_period("M")
counts = df.groupby("year_month").size().reset_index(name="post_count")

# Sort by date
counts = counts.sort_values("year_month")

# Calculate cumulative sum
counts["cumulative_posts"] = counts["post_count"].cumsum()

# Plot
plt.figure(figsize=(10,6))
plt.plot(counts["year_month"].astype(str), counts["cumulative_posts"], marker='o')
plt.xticks(rotation=45)
plt.xlabel("Month")
plt.ylabel("Cumulative Number of Posts")
plt.title("Cumulative Blog Posts Over Time")
plt.grid(True)
plt.tight_layout()

# Save plot image
chart_file = "cumulative_blog_posts.png"
plt.savefig(chart_file)
plt.close()

# Generate simple HTML embedding the image
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cumulative Blog Posts Over Time</title>
</head>
<body>
    <h1>Cumulative Blog Posts Over Time</h1>
    <img src="{chart_file}" alt="Cumulative Blog Posts Over Time Chart" style="max-width:100%; height:auto;">
</body>
</html>
"""

# Save HTML file
with open("cumulative_blog_posts.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Chart saved as '{chart_file}' and HTML saved as 'cumulative_blog_posts.html'")
