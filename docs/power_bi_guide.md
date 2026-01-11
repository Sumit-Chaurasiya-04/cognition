# Power BI Reporting Guide

You can visualize your Cognition data in Microsoft Power BI.

1.  **Export Data:**
    Run `python scripts/export_data.py`. This creates `cognition_export.xlsx`.

2.  **Import to Power BI:**
    * Open Power BI Desktop.
    * Click **"Get Data"** -> **"Excel Workbook"**.
    * Select `cognition_export.xlsx`.

3.  **Suggested Visualizations:**
    * **Word Cloud:** Import the "Word Cloud" visual. Drag the `Content` column into it to see most frequent terms in your knowledge base.
    * **Source Distribution:** Create a **Pie Chart**. Drag `Source` to the Legend and `ID` (Count) to Values. This shows which files contribute the most knowledge chunks.
    * **Search Simulation:** Add a **Text Filter** slicer on the `Content` column to mimic searching within Power BI.