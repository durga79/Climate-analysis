# Project Report: Climate Analytics & Economic Development
**[Your Name], [Your Student ID], [Group Name]**

## Executive Summary
This project delivers a comprehensive data analytics and visualization platform designed to investigate the correlation between economic development and environmental sustainability. The system (Climate Analytics Portal) provides users (Data Analysts and Researchers) with the ability to programmatically acquire historical data from the World Bank API, process it through a robust ETL pipeline, and visualize complex relationships through an interactive dashboard. The application implements best practices in data engineering across its entire development process, utilizing a technology stack comprising Python, MongoDB (for semi-structured raw data), and PostgreSQL (for structured analytical data). Key features include automated data ingestion, statistical and machine learning analysis (Clustering, Regression), and a responsive user interface built with Plotly Dash. The project demonstrates the effective handling of large datasets (>11,000 records) while ensuring data integrity, scalability, and maintainability.

## 1. Introduction
The Climate Analytics & Economic Development project provides a suite of analytical tools to explore how economic indicators (GDP, Population) influence environmental metrics (CO2, Renewable Energy). The main purpose of this project is to address the challenge of disparate data sources by creating a unified, automated pipeline that transforms raw, semi-structured API data into actionable insights. This application was designed to meet the rigorous standards of the Analytics Programming module, ensuring that data is handled programmatically at every stage—from acquisition and storage to cleaning, analysis, and visualization—while answering the core research question regarding the trade-offs between growth and sustainability.

## 2. Methodology
The project followed an iterative data science lifecycle (OSEMN: Obtain, Scrub, Explore, Model, Interpret). A modular architecture, built with Python scripts, object-oriented database handlers, and a Dash frontend, allowed the development team to implement distinct phases of the data pipeline. In addition to manual code reviews, automated unit testing (`pytest`) was employed to verify data quality and pipeline integrity. The developers implemented structured validation stages using Pandas and custom logging to ensure that data anomalies (missing values, outliers) were addressed systematically before analysis.

## 3. Requirements
The requirement specification for the Climate Analytics Portal consists of functional, non-functional, and system requirements. These requirements ensure the platform operates reliably as a data engineering tool while providing accurate analytical results.

### 3.1 Functional Requirements
**Data Acquisition & Storage**
*   Programmatically fetch historical data (2000-2023) for 30+ countries from the World Bank API.
*   Store raw, semi-structured JSON responses in a NoSQL database (MongoDB).
*   Extract raw data, transform it (cleaning, pivoting), and load it into a Relational database (PostgreSQL).

**Analysis & Machine Learning**
*   Calculate descriptive statistics and correlation matrices for key indicators.
*   Perform Machine Learning tasks: K-Means Clustering to group countries and Regression to predict trends.
*   Identify sustainability leaders based on composite scores.

**Visualization (Dashboard)**
*   Display interactive time-series charts for trends over time.
*   Render scatter plots to visualize GDP vs. Energy correlations.
*   Provide filtering capabilities by Country and Year range.

### 3.2 Non-Functional Requirements
*   **Data Integrity:** Ensure zero data loss during ETL; validate all data types before loading to PostgreSQL.
*   **Performance:** The dashboard must render visualizations in under 2 seconds.
*   **Reliability:** The pipeline must handle API failures gracefully using retry logic (exponential backoff).
*   **Maintainability:** Modular code structure using Python classes (`DataExtractor`, `DataTransformer`) and separate configuration files.
*   **Scalability:** The database schema must support adding new indicators or countries without major refactoring.

### 3.3 System Users
*   **Data Engineers:** Execute the pipeline scripts to update the database.
*   **Analysts/End Users:** Interact with the dashboard to explore trends and insights.

### 3.4 Use Case Descriptions
*   **Run Pipeline:** Engineer executes `run_full_pipeline.bat` → System fetches data → Stores in MongoDB → Cleans → Loads to Postgres → Runs Analysis.
*   **View Analysis:** Analyst opens Dashboard → Selects "United States" and "China" → Views comparative CO2 trends.
*   **Check Correlations:** Analyst views Heatmap → Identifies strong correlation between GDP and Energy Use.

### 3.5 Use Case Diagram
*(Description for Diagram)*: The diagram would show the **Data Engineer** initiating the **ETL Pipeline**. The Pipeline interacts with **World Bank API**, **MongoDB**, and **PostgreSQL**. The **Analyst** interacts with the **Dashboard**, which queries **PostgreSQL** to display charts.

### 3.6 Security & Data Quality Requirements
**Data Validity**
*   All API responses must be validated for JSON structure before storage.
*   Missing values must be handled via forward/backward filling, not dropped indiscriminately.

**Configuration Security**
*   Database credentials (URI, Passwords) must be stored in environment variables (`.env`), never hardcoded.
*   API connection parameters must be configurable without code changes.

**Error Handling**
*   Network errors during fetching must trigger retries, not crashes.
*   Database connection failures must be logged with specific error messages.

## 4. System Design and Architecture

### 4.1 System Architecture Overview
The project was built with a modern data engineering architecture. It leverages **Python 3.10+** for the core logic, **MongoDB** for the Data Lake (Raw Layer), and **PostgreSQL** for the Data Warehouse (Processed Layer). Each layer is well-defined:
1.  **Acquisition Layer:** Scripts in `src/data_acquisition/` handle API communication.
2.  **Storage Layer:** `MongoDBHandler` and `PostgresHandler` classes manage database interactions.
3.  **Processing Layer:** The ETL pipeline (`src/etl/`) transforms JSON documents into normalized SQL tables.
4.  **Analysis Layer:** `scikit-learn` and `scipy` scripts perform statistical modeling.
5.  **Presentation Layer:** A **Plotly Dash** web application serves the UI.

### 4.2 Data Flow Diagram (DFD)
*(Refer to Diagram)*: Data flows from External Source (API) -> Python Fetcher -> MongoDB (JSON) -> ETL Processor (Pandas) -> PostgreSQL (Tables) -> Analysis Scripts -> Dashboard UI.

### 4.3 Threat Model and Secure Design Principles
While primarily an analytics project, secure design principles were applied:
*   **Credential Isolation:** Addressed by using `python-dotenv` to load secrets.
*   **Data Integrity:** Prevented corruption using transaction-like processing in ETL (only committing after successful transformation).
*   **Availability:** ensured by robust error handling in the API fetchers to prevent pipeline termination on transient network issues.

### 4.4 Component Design
The architecture uses a **modular design pattern**.
*   **`src/database/`**: Contains Singleton-like classes for database connections to ensure resource efficiency.
*   **`src/etl/`**: Separates concerns into `extract.py`, `transform.py`, and `load.py`.
*   **`dashboard/`**: Uses a callback-based structure to update charts dynamically based on user input.

### 4.5 User Interface Overview
The user interface is a web-based dashboard running on `http://127.0.0.1:8050`. It features a sidebar for controls (Year Slider, Country Dropdown) and a main content area with a grid of visualizations (Line Charts, Scatter Plots, Heatmaps). The UI is built with **Dash Bootstrap Components** for responsiveness.

## 5. Implementation

### 5.1 Overview of Backend Implementation
The backend implementation centers on the **ETL Pipeline**. It separates concerns into clear layers: Data Ingestion (Requests), Data Storage (Pymongo/SQLAlchemy), and Logic (Pandas). The pipeline uses `pandas` DataFrames as the primary data structure for in-memory manipulation before persisting to PostgreSQL.

### 5.2 Database Implementation
The system implements a **Polyglot Persistence** architecture.
*   **MongoDB (Raw):** Stores the nested JSON responses from the World Bank API exactly as received. This ensures we have a pristine backup of the source data.
*   **PostgreSQL (Processed):** Uses a Star Schema design with a central `combined_analysis` table joined with metadata tables. This is optimized for the complex SQL queries required by the dashboard.

### 5.3 Implementation of Analysis Features
Dedicated scripts (`statistical_analysis.py`, `ml_models.py`) handle the analytical logic.
*   **Statistical:** Uses `scipy.stats` to calculate Pearson and Spearman correlations.
*   **Machine Learning:** Implements `sklearn.cluster.KMeans` to group countries into 4 distinct "sustainability clusters" based on their GDP and Renewable Energy metrics.
*   **Regression:** Uses `RandomForestRegressor` to determine feature importance (e.g., how much GDP predicts CO2 levels).

### 5.4 Input Validation, Error Handling, and Logging
The pipeline implements rigorous validation. The `DataTransformer` class checks for missing columns and invalid data types before merging datasets. Global error handlers catch exceptions (like Database Connection Refused) and log full stack traces to the console using Python's `logging` module.

### 5.5 Frontend Implementation (Dash)
The frontend is built with **Plotly Dash**. It communicates with the PostgreSQL database via the `PostgresHandler`. Callbacks are triggered by user interactions (e.g., moving the year slider), which executes a parameterized SQL query to fetch filtered data and updates the `dcc.Graph` components in real-time.

## 6. Testing

### 6.1 Functional Testing
Functional testing verified that the entire pipeline runs end-to-end. Scenarios included running the fetch scripts, verifying record counts in MongoDB, running the ETL, and checking the final row counts in PostgreSQL. A summary is provided in Appendix B (Table 1).

### 6.2 Data Quality & Integrity Testing
Testing verified the mitigation of common data issues (Duplicates, Missing Values). Unit tests (`tests/test_data_quality.py`) asserted that the final dataset contains no null values in critical columns and that year ranges are within 2000-2023. A summary is provided in Appendix B (Table 2).

### 6.3 Error Handling Tests
Tests confirmed that the application handles API downtimes by retrying and logs database errors without crashing. It was verified that the dashboard displays an empty state rather than crashing if no data is found for a filter.

### 6.4 Static Analysis
The process involved using `pnpm` (or pip) to manage dependencies and keeping `requirements.txt` updated. Manual code reviews confirmed that SQL queries are constructed safely using ORM methods (SQLAlchemy) rather than raw string concatenation.

### 6.5 Summary of Test Outcomes
The results verify that the system successfully ingests, processes, and visualizes the target datasets. The combination of automated unit tests and manual validation ensures accurate analytical results.

## 7. Conclusion and Future Work
The Climate Analytics Portal demonstrates how to build a robust data engineering solution using modern Python tools. All features were designed with "Modularity" and "Data Integrity" principles. The project proves that combining NoSQL and SQL databases provides the flexibility to handle semi-structured API data while supporting complex analytics. Future enhancements will include: Deployment to a cloud server (AWS/Heroku), integration of more granular data sources (Weather API), and adding forecasting models to predict future CO2 trends.

## References
1.  McKinney, W. (2010). Data Structures for Statistical Computing in Python. *Proceedings of the 9th Python in Science Conference*.
2.  PostgreSQL Global Development Group. (2024). *PostgreSQL 16 Documentation*.
3.  World Bank Group. (2024). *World Bank Open Data API*. https://data.worldbank.org/
4.  Plotly Technologies Inc. (2015). *Collaborative Data Science*. https://plot.ly.
5.  Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, pp. 2825-2830.
6.  Van Rossum, G., & Drake, F. L. (2009). *Python 3 Reference Manual*. Scotts Valley, CA: CreateSpace.

---

## Appendix B — Testing Tables

### Table 1. Functional Testing Summary

| Test Case | Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Data Fetching** | Fetch data for 30 countries | API returns JSON, saved to MongoDB | 11,520 records stored | **Pass** |
| **ETL Transformation** | Clean and Merge Datasets | Unified DataFrame created | 720 clean rows produced | **Pass** |
| **Database Load** | Load data to PostgreSQL | Tables created and populated | 5 tables populated | **Pass** |
| **Analysis** | Run Correlation Analysis | Correlation matrix generated | Matrix logged to console | **Pass** |
| **Dashboard Launch** | Start Web Server | Server starts on port 8050 | Accessible at localhost | **Pass** |
| **Filtering** | Filter Dashboard by Year | Charts update to show range | Charts updated correctly | **Pass** |

### Table 2. Data Quality & Security Testing Summary

| Vulnerability/Risk | Test Method | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Missing Data** | Run ETL with partial data | Pipeline fills/interpolates | Zero nulls in final set | **Pass** |
| **Duplicate Data** | Insert duplicate records | ETL removes duplicates | Unique rows preserved | **Pass** |
| **SQL Injection** | (N/A) Internal App | Queries use ORM/Parameters | Secure DB access | **Pass** |
| **Credential Leak** | Check code for keys | Keys in `.env` only | No hardcoded secrets | **Pass** |
| **API Failure** | Simulate Network Error | Script retries connection | Retried 3 times | **Pass** |
| **Invalid Schema** | API changes format | Pipeline logs error | Error handled gracefully | **Pass** |

### Table 3. Error Handling and Logging Tests

| Test Type | Intent | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Database Down** | Stop MongoDB service | Script logs "Connection Failed" | "ConnectionRefused" logged | **Pass** |
| **Empty Dataset** | Run analysis on empty DB | Script exits with warning | Warned "No data found" | **Pass** |
| **Invalid Config** | Remove `.env` file | Script errors on startup | Error "Missing Config" | **Pass** |

---

## Appendix C — Project Requirements Completion Table

| Requirement ID | Requirement Description | Status | Completion % |
| :--- | :--- | :--- | :--- |
| **RQ-01** | Fetch data programmatically from API (2 datasets) | Completed | 100% |
| **RQ-02** | Store raw semi-structured data in MongoDB | Completed | 100% |
| **RQ-03** | Implement ETL pipeline (Clean, Transform, Merge) | Completed | 100% |
| **RQ-04** | Store structured data in PostgreSQL | Completed | 100% |
| **RQ-05** | Perform Statistical Analysis & Machine Learning | Completed | 100% |
| **RQ-06** | Develop Interactive Dashboard (Dash) | Completed | 100% |
| **RQ-07** | Implement Modular Architecture | Completed | 100% |
| **RQ-08** | comprehensive Documentation & Testing | Completed | 100% |

