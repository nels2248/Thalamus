import pandas as pd
import requests
import os
import re
from urllib.parse import urljoin, urlparse

# Load the Excel file
df = pd.read_excel("thalamus_blog_links.xlsx")

# Output directory for HTML files
output_dir = "blog_html"
os.makedirs(output_dir, exist_ok=True)

# Base URL to prepend if needed
base_url = "https://www.thalamusgme.com"

def slugify(url):
    """
    Converts a blog URL into a safe filename.
    Example: /blogs/ai-in-gme → ai-in-gme.html
    """
    parsed = urlparse(url)
    path = parsed.path
    slug = path.strip("/").split("/")[-1]
    return re.sub(r'[^a-zA-Z0-9_-]', '', slug) + ".html"

# Loop through each URL
for i, row in df.iterrows():
    partial_url = row["Blog Link"]
    full_url = urljoin(base_url, partial_url)

    filename = slugify(full_url)
    filepath = os.path.join(output_dir, filename)

    print(f"Downloading: {full_url} → {filename}")

    try:
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
    except Exception as e:
        print(f"❌ Failed to download {full_url}: {e}")

print("\n✅ Finished downloading blog HTML pages.")
