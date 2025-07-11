

import pandas as pd 
df = pd.read_excel("thalamus_blog_content.xlsx")

#convert date to actual date format
df["published_date"] = pd.to_datetime(df["published_date"])


df["word_count"] = df["content"].str.split().str.len()
df.set_index("published_date")["word_count"].resample("M").mean().plot(title="Average Word Count Over Time")
