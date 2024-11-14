# Project Plan

## Title
Impact of Mental Health on Marriage in the USA (2021 and 2022)

## Main Question
Does mental health, specifically mental illness and suicidality, impact marriage rates in different USA states?

## Description
With the growing focus on mental health, this project will examine whether there is a connection between mental health conditions, suicidality, and marriage rates. This study will explore if states with higher levels of mental illness or suicidality show different marriage rates. The goal is to determine if mental health challenges and thoughts of suicide in some states may relate to lower marriage rates.

## Note:
The data is set to be for 2021–2022; however, it appears that the tables were published in 2022, but most of the data from the second source is based on 2021. Therefore, I will further investigate whether to use the average of the data from source one for 2021 and 2022, or to use only 2021 data.

## Data Sources

### Datasource 1: Marriage Rates by State (2019-2022)
- **Metadata URL:** [https://www.cdc.gov/nchs/pressroom/sosmap/marriage_by_state/marriage_rates.htm](https://www.cdc.gov/nchs/pressroom/sosmap/marriage_by_state/marriage_rates.htm)
- **Data URL:** You can download the data from the link above, but only by clicking "Download CSV." The link itself cannot be copied directly, and it includes four Excel files for different years. Only 2021 and 2022 data will be used.
- **Data Type:** CSV or PDF
- **Data Type:** I could not download it with Beautifulsoup and selenium do pdf data were extracted from a fixed pdf link
- **Description:** This CDC dataset shows the number of marriages per 1,000 people in each U.S. state. It allows for a comparison of marriage rates between states, providing useful insights into marriage trends over recent years.

### Datasource 2: Mental Illness and Suicidality
- **Metadata URL:** [https://www.samhsa.gov/data/report/2021-2022-nsduh-state-prevalence-estimates](https://www.samhsa.gov/data/report/2021-2022-nsduh-state-prevalence-estimates)
- **Data URL:** [https://www.samhsa.gov/data/sites/default/files/reports/rpt44484/2022-nsduh-sae-tables-percent-CSVs/2022-nsduh-sae-tables-percent.xlsx](https://www.samhsa.gov/data/sites/default/files/reports/rpt44484/2022-nsduh-sae-tables-percent-CSVs/2022-nsduh-sae-tables-percent.xlsx).
- **Data Type:** Tables in XLSX
- **Description:** This dataset includes key mental health indicators by state, including:
  - **Mental Illness:**
    - Any Mental Illness in the Past Year (Table 31)
    - Serious Mental Illness in the Past Year (Table 32)
    - Received Mental Health Treatment in the Past Year (Table 33)
    - Major Depressive Episode in the Past Year (Table 34)
  - **Suicidality:**
    - Had Serious Thoughts of Suicide in the Past Year (Table 35)
    - Made Any Suicide Plans in the Past Year (Table 36)
    - Attempted Suicide in the Past Year (Table 37)

These indicators will be analyzed alongside marriage rates to identify any potential correlations.

## Data Preprocessing Requirements (Work Packages)
- **Some links are auto-generated:** ~~I will use BeautifulSoup to download the data in my Python script.~~ I found a fixed link to a PDF that has the data, so now the plan is to find a library that works with PDF texts, such as pdfplumber.
- **Restrict Age Group:** Since this project focuses on marriage, the data should be filtered to include individuals aged 18 and older.
- **Combine Data Sources:** The mental health and suicidality data will be combined with marriage rates data by state and year for comparison.
Note that, as the mental health and suicidality data is one table per year, the focus is to observe the states that were affected.
- **Project Steps:** After filtering and merging the data, analysis can begin to understand the impact of mental health and suicidality on marriage rates.