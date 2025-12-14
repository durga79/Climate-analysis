# Work Breakdown Report

**Module:** Data Mining & Machine Learning  
**Project:** Climate Analytics & Economic Development  
**Date:** December 2025

---

## Team Members

| Name | Student ID | Role |
| :--- | :--- | :--- |
| **Dattathreya Chintalapudi** | x24212881 | Data Engineer & Backend Developer |
| **Saatvik reddy Gutha** | x24257460 | Data Analyst & Frontend Developer |

---

## 1. Executive Summary of Contributions

The project workload was divided to leverage complementary skills while ensuring both members gained experience across the full stack (Data Engineering, Machine Learning, and Visualization). 

*   **Dattathreya (x24212881)** focused on the **Back-End Infrastructure**. He architected the "Polyglot" database system, built the API fetching logic, and implemented the robust ETL pipeline that ensures data quality.
*   **Saatvik (x24257460)** focused on the **Front-End & Analytics**. He developed the Machine Learning models (K-Means, Regression), interpreted the statistical results, and built the interactive Dash dashboard.

Both members collaborated on the final report writing and code integration.

---

## 2. Detailed Task Breakdown

### Dattathreya Chintalapudi (x24212881)
**Primary Responsibility: Data Engineering & Infrastructure**

1.  **Data Acquisition (`src/data_acquisition/`):**
    *   Developed the `WorldBankFetcher` class using Python's `requests` library.
    *   Implemented the **Pagination Logic** to recursively fetch all pages of API data.
    *   Added **Exponential Backoff** to handle network timeouts and API rate limits.

2.  **Database Management (`src/database/`):**
    *   Set up **MongoDB Atlas** and wrote the `MongoDBHandler` class for raw JSON storage.
    *   Set up **PostgreSQL (Neon Tech)** and wrote the `PostgresHandler` using SQLAlchemy.
    *   Designed the Star Schema for the `combined_analysis` table.

3.  **ETL Pipeline (`src/etl/`):**
    *   Wrote the `DataTransformer` class to clean and pivot the data.
    *   Implemented the **Time-Series Interpolation** logic (`ffill`/`bfill`) to fix missing values in 2020-2023.
    *   Created the pipeline orchestration script to link Extract, Transform, and Load steps.

---

### Saatvik reddy Gutha (x24257460)
**Primary Responsibility: Machine Learning & Visualization**

1.  **Machine Learning (`src/analysis/`):**
    *   Implemented **K-Means Clustering** to segment countries into 4 sustainability profiles.
    *   Developed the **Random Forest Regressor** to predict CO2 emissions.
    *   Conducted **Feature Importance** analysis to identify "Energy Use" as the key driver.

2.  **Dashboard Development (`dashboard/`):**
    *   Built the **Plotly Dash** application structure.
    *   Designed the UI layout using **Dash Bootstrap Components**.
    *   Wrote the Python **Callbacks** to make charts interactive (filtering by Country/Year).

3.  **Statistical Analysis:**
    *   Performed Pearson Correlation analysis on key indicators (GDP, Energy, Population).
    *   Generated the visualizations (Heatmaps, Scatter Plots) used in the final report.

---

## 3. Collaborative Efforts
*   **Code Review:** Both members reviewed each other's Pull Requests on GitHub to ensure code quality.
*   **Debugging:** Jointly solved the "Cross-Module Import" error and the "Kaleido Image Generation" issue.
*   **Report Writing:** Dattathreya wrote the Methodology section; Saatvik wrote the Results & Evaluation section.

## 4. Sign-Off
We confirm that this breakdown accurately reflects the work distribution for this project.

*   **Dattathreya Chintalapudi:** ___________________
*   **Saatvik reddy Gutha:** ___________________

