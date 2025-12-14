# Project Walkthrough & Technical Cheat Sheet

**Use this guide to prepare for your presentation and viva. It explains exactly what each file does and why.**

---

## ⚡ The High-Level Data Flow (Memorize This!)
1.  **API** (World Bank) →
2.  **MongoDB** (Raw JSON "Data Lake") →
3.  **Python ETL** (Cleaning & Pivoting) →
4.  **PostgreSQL** (Structured "Data Warehouse") →
5.  **ML & Dashboard** (Final Analysis)

---

## 🟢 Phase 1: Getting the Data (Data Acquisition)
**Location:** `src/data_acquisition/`
*   **File:** `fetch_climate_data.py` (and `fetch_economic_data.py`)
*   **What it does:**
    1.  Connects to the **World Bank API**.
    2.  **Pagination Loop:** The API only gives 50 records per page. This script runs a `while` loop to say "Give me page 1, now page 2..." until it has all 20+ years of data.
    3.  **Retry Logic:** If the internet fails, it implements **Exponential Backoff** (waits 1s, 2s, 4s) and tries again.
*   **Key Technical Term:** "Programmatic Ingestion" and "Resilient API Consumption".

## 🟡 Phase 2: Storing Raw Data (The Data Lake)
**Location:** `src/database/mongodb_handler.py`
*   **What it does:**
    1.  Takes the messy, nested JSON response directly from the API.
    2.  Inserts it into **MongoDB** collections (`climate_raw`, `economic_raw`).
*   **Why MongoDB?** Because the data is **Semi-Structured**. We want to store the "Source of Truth" exactly as it arrived without breaking it.

## 🟠 Phase 3: Cleaning & Transforming (The ETL Core)
**Location:** `src/etl/transform.py`
*   **What it does:** This is the heaviest logic in the project.
    1.  **Pivoting:** The raw data is "Long" (one row per year per indicator). This script flips it to "Wide" (Years as rows, Indicators as columns) so it looks like a spreadsheet.
    2.  **Cleaning:** It removes duplicates and drops empty columns.
    3.  **Handling Missing Data:** Crucial Step! For years like 2023 where data might be missing, it uses **Time-Series Interpolation** (`ffill` - Forward Fill). It copies the 2022 value forward so the ML models don't crash.
    4.  **Feature Engineering:** Creates new columns like `renewable_adoption_category` (High/Medium/Low) for better analysis.

## 🔵 Phase 4: Storing Clean Data (The Data Warehouse)
**Location:** `src/database/postgres_handler.py` & `src/etl/load.py`
*   **What it does:**
    1.  Takes the clean Pandas DataFrame.
    2.  Saves it into **PostgreSQL** in a table called `combined_analysis`.
*   **Why Postgres?** Because now the data is **Structured** (rows and columns). SQL databases are much faster for the dashboard to query than scanning JSON files.

## 🟣 Phase 5: The Brains (Machine Learning)
**Location:** `src/analysis/ml_models.py`
*   **What it does:**
    1.  **Clustering (K-Means):** Groups countries into 4 categories based on GDP and Renewable Energy. (e.g., finding the "Green Leaders").
    2.  **Regression (Random Forest):** Predicts CO2 emissions based on other factors.
    3.  **Feature Importance:** Calculates *which* factor matters most. It found that **Energy Use** (72%) is more important than **GDP** (5%) for predicting emissions.

## 🔴 Phase 6: The Face (The Dashboard)
**Location:** `dashboard/app.py`
*   **What it does:**
    1.  Runs a web server using **Plotly Dash**.
    2.  **Callbacks:** When you move the "Year Slider", a Python function triggers, queries the Postgres database, filters the data, and updates the graphs instantly.
    3.  **Visuals:** Draws the Correlation Heatmap and Trend Lines.

---

## 📝 Common Questions & Answers

**Q: Why did you use two databases?**
**A:** We used a **Polyglot Persistence** architecture. MongoDB is best for ingesting the messy, semi-structured API data (High Write Speed). PostgreSQL is best for the structured, clean data required by our Dashboard and ML models (High Read Speed/SQL Joins).

**Q: How did you handle missing data?**
**A:** We used **Forward Fill (ffill)** and **Backward Fill (bfill)**. Since economic data doesn't change drastically year-over-year, it is statistically valid to assume the 2023 value is similar to 2022 if the API hasn't updated yet.

**Q: What was the hardest part?**
**A:** Handling the API rate limits and fixing the Python module import errors when running scripts from different folders (solved using `sys.path`).

