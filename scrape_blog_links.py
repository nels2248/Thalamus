import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# Base URL (adjust if needed)
base_url = "https://www.thalamusgme.com/blogs"

blog_links = []

# Loop through pages 1 to 11
for page in range(1, 12):
    url = f"{base_url}?785a8a27_page={page}"
    print(f"Scraping: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error on page {page}: {e}")
        continue

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags with blog links
    for a in soup.find_all("a", href=True):
        href = a["href"] 
        if "/blogs/" in href:
            blog_links.append(href)

    time.sleep(1)  # Be polite to the server

# Remove duplicates
unique_links = sorted(set(blog_links))

# Create a DataFrame
df = pd.DataFrame(unique_links, columns=["Blog Link"])

# Save to Excel
excel_file = "thalamus_blog_links.xlsx"
df.to_excel(excel_file, index=False)

print(f"\n✅ Saved {len(unique_links)} blog links to '{excel_file}'")
