import os
import pandas as pd
from bs4 import BeautifulSoup

# Folder where HTML files are stored
html_dir = "blog_html"

# Lists to store data
contents = []
dates = []
filenames = []

# Loop through each HTML file
for filename in os.listdir(html_dir):
    if not filename.endswith(".html"):
        continue

    filepath = os.path.join(html_dir, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        # Extract blog content
        content_div = soup.find("div", class_="blog_rich-text w-richtext")
        content_text = content_div.get_text(separator="\n", strip=True) if content_div else ""

        # Extract publish date
        date_block = soup.find("div", class_="date_publish-block")
        if date_block:
            published_dates = date_block.find_all("div", class_="published_date")
            if len(published_dates) >= 2:
                date_text = published_dates[1].get_text(strip=True)
            else:
                date_text = ""
        else:
            date_text = ""

        contents.append(content_text)
        dates.append(date_text)
        filenames.append(filename)

# Create DataFrame
df = pd.DataFrame({
    "filename": filenames,
    "published_date": dates,
    "content": contents
})

# Save to Excel (or CSV if preferred)
df.to_excel("thalamus_blog_content.xlsx", index=False)

print(f"✅ Extracted {len(df)} blog posts into 'thalamus_blog_content.xlsx'")
