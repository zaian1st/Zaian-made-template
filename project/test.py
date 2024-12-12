import os
import re
import sqlite3
import pandas as pd
import pytest
import requests
import pdfplumber
from io import BytesIO
import subprocess

# URLs for the data sources
pdf_url = "https://www.cdc.gov/nchs/data/dvs/marriage-divorce/state-marriage-rates-90-95-00-22.pdf"
excel_url = "https://www.samhsa.gov/data/sites/default/files/reports/rpt44484/2022-nsduh-sae-tables-percent-CSVs/2022-nsduh-sae-tables-percent.xlsx"

def test_load_pdf_data():  # Unit Tests 
    """
    Test if the marriage rates data can be successfully extracted from the PDF.
    """
    response = requests.get(pdf_url)
    response.raise_for_status()
    
    data = []
    with pdfplumber.open(BytesIO(response.content)) as pdf:
        page = pdf.pages[0]  # Get the first page of the PDF
        text = page.extract_text()
        pattern = r"^([A-Za-z\s]+)\s+([\d.]+)\s+([\d.]+)"
        for line in text.split("\n"):
            match = re.match(pattern, line)
            if match:
                state = match.group(1).strip()
                rate_2022 = float(match.group(2))
                rate_2021 = float(match.group(3))
                data.append([state, rate_2022, rate_2021])
    
    assert len(data) > 0, "No data extracted from the PDF"
    assert all(isinstance(row[1], float) for row in data), "Marriage rates are not floats"

def test_load_excel_data():
    """
    Test if the mental health data can be successfully loaded from the Excel file.
    """
    sheet_info = {
        "Table 31": 5,
        "Table 32": 5,
        "Table 33": 6,
        "Table 34": 6,
        "Table 35": 5,
        "Table 36": 5,
        "Table 37": 5
    }
    
    for sheet, skip_rows in sheet_info.items():
        df = pd.read_excel(excel_url, sheet_name=sheet, skiprows=skip_rows)
        assert not df.empty, f"Sheet {sheet} is empty"
        assert "State" in df.columns, "State column is missing in the Excel data"
        
def test_system():
    # Define the expected output database file path
    database_full_path = os.path.join(os.path.dirname(__file__), "../data/merged_mental_marriage_data.sqlite")

    # Ensure the output directory exists
    output_dir = os.path.dirname(database_full_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run the pipeline script (correct path for pipeline.py)
    pipeline_path = os.path.join(os.path.dirname(__file__), "pipeline.py")
    result = subprocess.run(["python", pipeline_path], capture_output=True, text=True)

    # Assert that the pipeline executed successfully
    assert result.returncode == 0, f"Pipeline execution failed with error:\n{result.stderr}"

    # Validate that the database file was created
    assert os.path.exists(database_full_path), f"Output database file not found at {database_full_path}"




def test_merge_dataframes(): # Integration Tests
    """
    Test if marriage rates and mental health data can be merged correctly.
    """
    # Mock marriage rates data
    df_pdf = pd.DataFrame({
        "State": ["Alabama", "Alaska"],
        "Marriage rates per 1,000 in 2022": [7.2, 6.3],
        "Marriage rates per 1,000 in 2021": [6.8, 5.9]
    })

    # Mock mental health data
    df_mental_health = pd.DataFrame({
        "State": ["Alabama", "Alaska"],
        "Any Mental Illness 18+ (%)": [20.1, 22.5]
    })

    # Merge data
    merged_df = pd.merge(df_pdf, df_mental_health, on="State", how="inner")
    assert not merged_df.empty, "Merged DataFrame is empty"
    assert "State" in merged_df.columns, "State column is missing after merge"
    assert "Marriage rates per 1,000 in 2022" in merged_df.columns, "Marriage rate column is missing"
    assert "Any Mental Illness 18+ (%)" in merged_df.columns, "Mental health column is missing"


# Run all tests with pytest
if __name__ == "__main__":
    pytest.main()
