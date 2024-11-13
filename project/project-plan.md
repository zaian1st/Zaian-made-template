# Project Plan

## Title
Impact of Mental Health on Marriage in the USA (2021  and 2022)

## Main Question
Does mental health scoping it to (4 mental illness only constraints), impact marrige rates in diffrent USA States?

## Description
With the growing focus on mental health, this project will examine whether there is a connection between mental health conditions, suicidality, and marriage rates. This study will explore if states with higher levels of mental illness or suicidality show different marriage rates. The goal is to determine if mental health challenges and thoughts of suicide in some states may relate to lower marriage rates.

## Data Sources

### Datasource 1: Marriage Rates by State (2019-2022)
- **Metadata URL:** [https://www.cdc.gov/nchs/pressroom/sosmap/marriage_by_state/marriage_rates.htm](https://www.cdc.gov/nchs/pressroom/sosmap/marriage_by_state/marriage_rates.htm)
- **Data URL:** You can download the data from the link above, but only by clicking "Download CSV." The link itself cannot be copied directly, and it includes 4 Excel files for different years. Only  2021 and 2022 data will be used.
- **Data Type:** CSV
- **Description:** This CDC dataset shows the number of marriages per 1,000 people in each U.S. state. It lets you compare marriage rates between states. This data is helpful for studying marriage trends over the past few years.

### Datasource 2: Mental Illness and Suicidality
- **Metadata URL:** [https://www.samhsa.gov/data/report/2021-2022-nsduh-state-prevalence-estimates](https://www.samhsa.gov/data/report/2021-2022-nsduh-state-prevalence-estimates)
- **Data URL:** [https://www.samhsa.gov/data/sites/default/files/reports/rpt44484/2022-nsduh-sae-tables-percent-CSVs/2022-nsduh-sae-tables-percent.xlsx](https://www.samhsa.gov/data/sites/default/files/reports/rpt44484/2022-nsduh-sae-tables-percent-CSVs/2022-nsduh-sae-tables-percent.xlsx).
- **Data Type:** tables in xlsx
- **Description:** This dataset includes key mental health indicators by state, such as:
  - **Mental Illness:(4 constraints)**
    - Any Mental Illness in the Past Year (Table 31)
    - Serious Mental Illness in the Past Year (Table 32)
    - Received Mental Health Treatment in the Past Year (Table 33)
    - Major Depressive Episode in the Past Year (Table 34)

These indicators will be analyzed alongside marriage rates to identify any potential correlations.

## Data Preprocessing Requirements (Work Packages)
- **Some links are Auto generated:** ~~I will be use beautifulsoup to download the data in my bython script~~ I found a fixed link of pdf that has the data then the idea now is to find a library that work with pdf texts like pdfplumber
- **Restrict Age Group:** Since this project focuses on marriage, the data should be filtered to include individuals aged 18 and older.
- **Combine Data Sources:** The mental health and suicidality data will be combined with marriage rates data by state and year for comparison.
Note since mental health and suicidality data is one table per one year so the scope part is to see the states taht got effected .
- **Project Steps:** After filtering and merging the data, analysis can begin to understand the impact of mental health and suicidality on marriage rates.
