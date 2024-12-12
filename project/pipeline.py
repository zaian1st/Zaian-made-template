''' My goal : Write a script that pulls the data sets , transforms it and fixes errors, and finally stores your data in the /data directory
Write data into a SQLite database called “merged_mental_marriage_data.sqlite”, in the table “Mental_Marriage_Data”
I couldnt use bs4 to parse the dynamic button and I found a solution to have selinium as it works like a webdrive but
then if I use chrome drive locally then there will not be aoutomated code to run in venv I guess not sure cuse it needs my 
chrome.exe directory so I thought that is not a good soloution 
BUT I found the same data in a static link but in PDF which then solves my problem but its PDF not a structured data format
However lucky me it was one page and I could find a libray that extract the text and help me to save it and merge it 
// I will rename some column names as I will merge the data from 5 tables
// I will Assign fitting built-in SQLite types (e.g., TEXT or FLOAT) to all other columns
// and finally stores your data in the /data directory
https://docs.python.org/3/library/re.html
https://docs.python-requests.org/en/master/
https://pandas.pydata.org/docs/
https://docs.python.org/3/library/io.html
https://docs.python.org/3/library/sqlite3.html
'''
import os
import re  
import requests 
import pdfplumber  
import pandas as pd  
from io import BytesIO  
import sqlite3  
import time

# URLs for the data sources (one PDF, one Excel file)
pdf_url = "https://www.cdc.gov/nchs/data/dvs/marriage-divorce/state-marriage-rates-90-95-00-22.pdf"
excel_url = "https://www.samhsa.gov/data/sites/default/files/reports/rpt44484/2022-nsduh-sae-tables-percent-CSVs/2022-nsduh-sae-tables-percent.xlsx"

# Step 1: Load Marriage Rates data from PDF
# Fetch PDF data from the URL
response = requests.get(pdf_url)
response.raise_for_status()  # Raise an error if the download fails

'''def fetch_data_with_retry(url, retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise error if the request fails
            return response.content
        except requests.RequestException as e:
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    raise Exception(f"Failed to fetch data from {url} after {retries} attempts.")'''


# Extract marriage rate data for each state (2022 and 2021) from PDF
data = []
with pdfplumber.open(BytesIO(response.content)) as pdf:
    page = pdf.pages[0]  # Get the first (and only) page of the PDF
    text = page.extract_text()  # Extract text from the page
    
    # This is kinda like regex from ex2.jv to show how the data look in the pdf  
    # To find state names and Marriage rates
    pattern = r"^([A-Za-z\s]+)\s+([\d.]+)\s+([\d.]+)"
    for line in text.split("\n"):
        match = re.match(pattern, line)
        if match:
    # Since the pdf is extracting text I will assign float to  Marriage rates  
            state = match.group(1).strip()
            rate_2022 = float(match.group(2))
            rate_2021 = float(match.group(3))
            data.append([state, rate_2022, rate_2021])

# Convert the data to a DataFrame for easy handling
# Also I renamed the header names to make sure the data wont misunderstood
df_pdf = pd.DataFrame(data, columns=[
    "State", 
    "Marriage rates per 1,000 in 2022", 
    "Marriage rates per 1,000 in 2021"
])

# Step 2: Load Mental Health Data and Suicide from Excel
# Each sheet requires specific rows to skip at the top
# These will be the sheets I am intersted in 
sheet_info = {
    "Table 31": 5,
    "Table 32": 5,
    "Table 33": 6,
    "Table 34": 6,
    "Table 35": 5,
    "Table 36": 5,
    "Table 37": 5
}

# Columns to remove from the tables that have data we don’t need
columns_to_drop = [
    "12-17\nEstimate", 
    "12-17\n95% CI (Lower)", 
    "12-17\n95% CI (Upper)",
    "18+\n95% CI (Lower)", 
    "18+\n95% CI (Upper)",
    "18-25\n95% CI (Lower)", 
    "18-25\n95% CI (Upper)",
    "26+\n95% CI (Lower)", 
    "26+\n95% CI (Upper)"
]

# Mapping of sheet names to categories (used to rename columns later)
# This part is important as the data when it merged will have the same header name we need to prevent this 
constraint = {
    "Table 31": "Any Mental Illness",
    "Table 32": "Serious Mental Illness",
    "Table 33": "Received Mental Health Treatment",
    "Table 34": "Major Depressive Episode",
    "Table 35": "Thoughts of Suicide",
    "Table 36": "Made Any Suicide Plans",
    "Table 37": "Attempted Suicide"
}

# Dictionary to hold cleaned data from each sheet
dfs = {}

# Process each sheet based on the given information
for sheet, skip_rows in sheet_info.items():
    df = pd.read_excel(excel_url, sheet_name=sheet, skiprows=skip_rows)
    state_column = df.columns[1]  # Assume the second column has state names
    df = df.dropna(subset=[state_column])  # Remove rows with no state name
    
    # Drop unnecessary columns if they are present in the table
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors="ignore")
    
    # Remove the "Total U.S." row as it’s not relevant to our state-by-state analysis
    df = df[df[state_column] != "Total U.S."]
    df = df.sort_values(by=state_column).reset_index(drop=True)  # Sort alphabetically by state name
    
    # Rename columns to include category names and multiply by 100 for percentage
    category_name = constraint[sheet]
    df = df.rename(columns={
        "18+\nEstimate": f"{category_name} 18+ (%)",
        "18-25\nEstimate": f"{category_name} 18-25 (%)",
        "26+\nEstimate": f"{category_name} 26+ (%)"
    })
    
    # Multiply percentage columns by 100 for readability as we want it as "(%)"
    for col in df.columns:
        if "(%)" in col:
            df[col] = pd.to_numeric(df[col], errors="coerce") * 100  
    
    # Save cleaned data for the current sheet
    dfs[sheet] = df

# Step 3: Merge all Mental Health Tables
# Start with the first table (Table 31) and merge others on "State"
merged_df = dfs["Table 31"]
for sheet in ["Table 32", "Table 33", "Table 34", "Table 35", "Table 36", "Table 37"]:
    merged_df = merged_df.merge(dfs[sheet], on=["Order", "State"], how="outer")

# Remove the "Order" column and ensure "State" is a string
merged_df = merged_df.drop(columns=["Order"])
merged_df["State"] = merged_df["State"].astype(str)

# Remove any rows with missing data (NaN values)
merged_df = merged_df.dropna()

# Step 4: Merge Marriage Rates Data with Mental Health Data
# Keep only states present in the marriage rate data
# https://www.ionos.at/digitalguide/websites/web-entwicklung/python-pandas-dataframe-isin/
# reference_states, returning only rows with a match. (True or False)
reference_states = set(df_pdf["State"])
merged_df = merged_df[merged_df["State"].isin(reference_states)]

# Merge marriage rates with mental health data on the "State" column
# how="inner" argument specifies an inner join, which means only states present in both df_pdf and merged_df
final_merged_df = pd.merge(df_pdf, merged_df, on="State", how="inner")

# Step 5: Save the Final Data to SQLite Database
# Connect to SQLite database and save final data to a table
# Ensure the data directory exists
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    
conn = sqlite3.connect(r'data/merged_mental_marriage_data.sqlite')
final_merged_df.to_sql('mental_Marriage_Data', conn, if_exists='replace', index=False)
conn.close()

# PRAGMA table_info(mental_Marriage_Data);
# I used it to make sure the data is clean not null and the types are correct 