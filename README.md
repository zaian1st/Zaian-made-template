# Impact of Mental Health on Marriage in the USA (2021/2022)  

## Overview  
This open-source project explores the relationship between mental health metrics and marriage rates in the United States for the years 2021 and 2022. The analysis focuses on identifying correlations between mental health factors (e.g., Serious Mental Illness, Suicidality) and state-level marriage trends.  

## Key Features  
- Data extracted and cleaned using **`pipeline.py`**.  
  - Creates an SQLite database (`merged_mental_marriage_data.sqlite`) with cleaned and merged data.  
- Analysis and visualizations conducted using **`Final_project.py`**.  
  - Generates correlation heatmaps, choropleth maps, scatterplots, and regression analysis outputs.  

---

## File Structure  
```plaintext
. please Ignore other folders as it relates to FAU MADE subject However the project files are
├─\project
 └── pipeline.py                                                     # ETL pipeline script
 └── Final_project.py                                                # Analysis and visualization script
 └── analysis-report.pdf                                             # Analysis findings and visualizations
 └── data-report.pdf                                                 # Data sources and cleaning process
 └── slides.pdf                                                      # project powepoint
├── /data                                                            # Directory containing the SQLite database
│   └── merged_mental_marriage_data.sqlite
├── /maps                                                            # Directory for analysis outputs (e.g., heatmaps, maps, CSV files)

```

---

## Installation  
To replicate or modify this project, install the required dependencies:  
```bash
pip install -r requirements.txt
```

---

## Usage  
### Step 1: Data Cleaning & Preparation  
Run the `pipeline.py` script to fetch, clean, and merge the datasets:  
```bash
python pipeline.py
```

### Step 2: Analysis & Visualization  
Run the `Final_project.py` script to generate visualizations and perform statistical analyses:  
```bash
python Final_project.py
```
Results will be saved in the `/maps` directory.

---

## Author  
👨‍💻 **Abdelrahman Zaian**  

---

## License  
This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.  

### Key Points  
- 📜 **Sharing & Adaptation:** You can share and adapt the work, provided you give appropriate credit.  
- 🚫 **No Commercial Use:** This project cannot be used for commercial purposes.  

For full license details, visit the [Creative Commons website](https://creativecommons.org/licenses/by-nc/4.0/).  

---

Feel free to contribute or suggest improvements! 🌟
