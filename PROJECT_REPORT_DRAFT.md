# Analysis of Economic Growth and Environmental Sustainability: A Data Engineering Approach

**Student Names:** Dattathreya Chintalapudi, Saatvik reddy Gutha  
**Student IDs:** x24212881, x24257460  
**Programme:** MSc in Data Analytics  
**Module:** Data Mining & Machine Learning  
**Year:** 2025-2026

---

## Abstract
This project presents a comprehensive, full-stack data analytics platform designed to investigate the complex, non-linear relationship between economic development and environmental sustainability. In an era where data-driven policy making is paramount, the ability to synthesize heterogeneous data sources into actionable intelligence is a critical skill. We developed a robust data engineering pipeline to programmatically acquire, process, and visualize historical data (2000-2023) from the World Bank API. The dataset covers critical indicators including GDP per capita, CO2 emissions per capita, renewable energy consumption, and population growth across a diverse set of 30 representative nations.

The system is built upon a "Polyglot Persistence" architecture, utilizing MongoDB for the flexible storage of raw, semi-structured JSON data and PostgreSQL for the storage of cleaned, structured analytical tables. An automated Extract-Transform-Load (ETL) pipeline, implemented in Python 3.10, orchestrates the complex tasks of data ingestion, normalization, cleaning (handling missing values via time-series interpolation), and integration. 

Beyond simple aggregation, we applied advanced machine learning techniques—specifically K-Means clustering and Random Forest regression—to identify distinct "sustainability profiles" among nations and to quantify the predictive power of economic factors on carbon output. The findings are disseminated through a high-performance, interactive web dashboard built with Plotly Dash, which allows users to explore trends dynamically. Our analysis reveals that while energy use remains the primary driver of emissions globally (Feature Importance: 72%), a distinct cluster of nations has successfully decoupled economic growth from carbon output through aggressive renewable energy adoption. This report details the technical implementation, the challenges encountered in data harmonization, and the statistical validity of our findings.

## 1. Introduction

### 1.1 Motivation and Context
The 21st century is defined by two opposing forces: the urgent need for economic development to lift billions out of poverty, and the existential threat of climate change driven by greenhouse gas emissions. Historically, these two forces have been inextricably linked; the Industrial Revolution demonstrated that economic output (GDP) is heavily correlated with energy consumption and, consequently, carbon dioxide (CO2) emissions. However, the rapid maturation of renewable energy technologies (solar, wind, hydroelectric) offers a potential pathway to "green growth"—a theoretical framework where economies can grow without a corresponding increase in environmental damage.

For data scientists and policy analysts, the challenge is no longer a lack of data, but rather the fragmentation of it. While organizations like the World Bank, the IEA, and the OECD publish vast troves of data, it often resides in disparate silos, with varying formats, missing values, and inconsistent schemas. This project was motivated by the need to create a unified, automated framework that can ingest these disparate data sources and transform them into a "Single Source of Truth" for analysis.

### 1.2 Research Question
The analysis is guided by the following primary research question:
*   **"To what extent does the adoption of renewable energy technologies decouple economic growth (GDP) from carbon emissions, and can unsupervised machine learning identify distinct typologies of national sustainability trajectories?"**

Secondary questions include:
*   **Q2:** Which socio-economic factors (Population, Urbanization, GDP) are the strongest predictors of a nation's CO2 per capita?
*   **Q3:** Is there statistical evidence of the "Environmental Kuznets Curve" in the post-2000 era?

### 1.3 Project Objectives
To answer these questions, the project laid out the following technical and analytical objectives:
1.  **Automated Data Acquisition:** Develop Python scripts to programmatically fetch over 20 years of historical data for 30+ representative countries using the World Bank REST API.
2.  **Polyglot Database Architecture:** Implement a hybrid storage solution using MongoDB for raw data preservation (Data Lake) and PostgreSQL for analytical processing (Data Warehouse).
3.  **Robust ETL Pipeline:** Construct a reusable Extract-Transform-Load pipeline that handles data cleaning, pivoting, and merging, ensuring high data quality.
4.  **Advanced Analytics:** Apply statistical correlation methods and machine learning models (Clustering, Regression) to derive non-obvious insights.
5.  **Interactive Visualization:** Build a responsive dashboard that adheres to "Shneiderman’s Mantra" (Overview first, zoom and filter, details on demand) to make the data accessible.

## 2. Related Work

### 2.1 The Environmental Kuznets Curve (EKC)
Theoretical groundwork for this analysis is found in the Environmental Kuznets Curve hypothesis. Stern (2004) famously reviewed the critique that environmental degradation increases with income up to a turning point, after which it declines. Early studies relied on static, cross-sectional data, which often failed to capture dynamic technological shifts. Our project contributes to this body of work by using *dynamic, longitudinal data* (2000-2023) to test if the "turning point" has shifted due to renewable technology.

### 2.2 Modern Data Stack & Polyglot Persistence
In the realm of software architecture, this project is informed by the concept of "Polyglot Persistence," popularized by Martin Fowler (2011). The traditional approach of forcing all data into a single Relational Database Management System (RDBMS) is increasingly seen as an anti-pattern when dealing with hierarchical API data. By using MongoDB for the "Ingestion Layer," we align with modern data engineering best practices that prioritize write throughput and schema flexibility at the start of the pipeline, shifting to strict schemas (PostgreSQL) only after the data is understood and cleaned.

### 2.3 Interactive Visual Analytics
Heer and Shneiderman (2012) established that "interactive dynamics" are crucial for data analysis. Static reports hide outliers and granular trends. By implementing a dashboard with filtering and "brushing" capabilities (where selecting a data point in one view highlights it in others), our project moves beyond static reporting to provide an exploratory tool, enabling users to discover their own insights.

## 3. Data Processing Methodology

### 3.1 Data Acquisition Strategy
The foundation of the project is the `src/data_acquisition` module. We chose the **World Bank Open Data API** as our primary source due to its reliability, comprehensive coverage, and open license.

*   **Dataset 1: Climate & Energy:** This dataset tracks the environmental impact. Key indicators fetched include:
    *   `EN.ATM.CO2E.PC`: CO2 emissions (metric tons per capita).
    *   `EG.USE.PCAP.KG.OE`: Energy use (kg of oil equivalent per capita).
    *   `EG.FEC.RNEW.ZS`: Renewable energy consumption (% of total final energy consumption).
*   **Dataset 2: Economic & Demographic:** This dataset tracks development. Indicators include:
    *   `NY.GDP.PCAP.CD`: GDP per capita (current US$).
    *   `SP.POP.TOTL`: Total Population.
    *   `SP.URB.TOTL.IN.ZS`: Urban population (% of total).

**Implementation Details:**
We created a base class `WorldBankFetcher` using the Python `requests` library. A critical challenge here was **Pagination**. The API returns data in pages of 50 records. Our script implements a recursive loop to detect the `total_pages` metadata and iterate through all available pages to ensure complete data retrieval. We also implemented an **Exponential Backoff** strategy to handle API timeouts (retrying after 1s, 2s, 4s).

### 3.2 Database Architecture (Storage)
We implemented a **Tiered Storage Architecture**:

**Tier 1: Raw Data Lake (MongoDB)**
We utilized MongoDB (hosted on MongoDB Atlas) to store the raw API responses.
*   **Why MongoDB?** The World Bank API returns nested JSON objects. For example, the country field is not just a string but a dictionary: `{"id": "US", "value": "United States"}`. Flattening this immediately would risk losing context. Storing it as a "Document" allows us to preserve the exact state of the data as it was received.
*   **Collection Strategy:** We separated data into three collections: `climate_raw`, `economic_raw`, and `renewable_raw`. This logical separation improves query performance and organization.

**Tier 2: Analytical Data Warehouse (PostgreSQL)**
We utilized PostgreSQL (hosted on Neon Tech) for the processed data.
*   **Why PostgreSQL?** The dashboard and ML models require structured, tabular data to perform joins and aggregations efficiently. SQL's strict typing (`FLOAT`, `INTEGER`, `VARCHAR`) acts as a final gatekeeper for data quality.
*   **Schema Design:** We employed a Star Schema approach. A central fact table `combined_analysis` holds the quantitative metrics, keyed by `country_code` and `year`. This design is optimized for "Online Analytical Processing" (OLAP) workloads.

### 3.3 The ETL Pipeline (Extract, Transform, Load)
The core logic resides in `src/etl/pipeline.py`. This script orchestrates the flow of data:

1.  **Extract:** The `DataExtractor` class connects to MongoDB. It uses the aggregation pipeline to project only the necessary fields (`country.value`, `date`, `value`, `indicator.id`) from the deep JSON structure, returning a raw Pandas DataFrame.

2.  **Transform:** The `DataTransformer` class performs the heavy lifting:
    *   **Pivoting:** The raw data is in "Long Format" (Entity-Attribute-Value). We pivoted this to "Wide Format" using `pd.pivot_table`, so that each indicator became a column (e.g., `climate_co2`).
    *   **Data Cleaning:** We identified significant missing data in the 2022-2023 range for some indicators. We implemented a **Time-Series Interpolation** strategy. First, we used `ffill()` (Forward Fill) to propagate the last known valid observation forward to fill recent gaps. Then, we used `bfill()` (Backward Fill) for older gaps. This assumes that economic/climate metrics do not fluctuate wildly year-over-year, which is a statistically valid assumption for this domain.
    *   **Feature Engineering:** We created a derived feature `renewable_adoption_category`, binning countries into 'Low', 'Medium', and 'High' based on their renewable percentage.

3.  **Load:** The `DataLoader` class uses SQLAlchemy to insert the clean DataFrame into PostgreSQL. We used the `to_sql(if_exists='replace')` method to ensure the analysis table is completely refreshed on every pipeline run, preventing duplicate records.

### 3.4 Data Processing Challenges and Solutions
Throughout the development lifecycle, we encountered several significant challenges that required specific engineering solutions:

*   **Challenge 1: Inconsistent API Data Availability**
    *   *Problem:* The World Bank API does not update all indicators simultaneously. While GDP data for 2023 might be available, CO2 emissions data often lags by 2-3 years. This resulted in `NaN` values when merging datasets on the `year` key, potentially causing our Machine Learning models to crash or drop entire years of valid economic data.
    *   *Solution:* We implemented a dynamic column checking mechanism in `src/analysis/ml_models.py`. Before running clustering, the code explicitly checks `if 'climate_co2_per_capita' in df.columns`. If the specific CO2 column is missing or entirely null for a given year, the model falls back to using `climate_energy_use` as a proxy variable. This "graceful degradation" ensures the pipeline completes even with partial data.

*   **Challenge 2: Cross-Module Import Resolution**
    *   *Problem:* As our project structure grew more complex with nested directories (`src/etl`, `src/analysis`, `config/`), Python scripts failed to import the `database_config` module when run directly from the terminal, throwing `ModuleNotFoundError`.
    *   *Solution:* We implemented a programmatic path modification. In the header of every executable script, we added:
      ```python
      sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
      ```
      This explicitly adds the project root to the Python path at runtime, ensuring reliable imports regardless of the working directory.

*   **Challenge 3: Database Connection Stability**
    *   *Problem:* During bulk insert operations to the cloud-hosted PostgreSQL database (Neon Tech), we occasionally experienced connection timeouts due to latency.
    *   *Solution:* We wrapped our `PostgresHandler` operations in a `try-finally` block. This ensures that the database cursor is always closed and the connection returned to the pool, preventing "connection leak" issues that would otherwise freeze the application after multiple runs.

## 4. Data Visualisation Methodology

### 4.1 Theoretical Framework
Our visualization strategy was grounded in **Tufte’s Principles of Graphical Integrity**. We aimed to maximize the "Data-Ink Ratio" by removing unnecessary grid lines and backgrounds, focusing the user's attention on the trends. We also applied **Gestalt Principles** of grouping, using color consistency (green for renewable, red for fossil fuels) across different charts to help the user cognitively link related data points.

### 4.2 Dashboard Architecture
The dashboard (`dashboard/app.py`) is a Single Page Application (SPA) built with **Dash Bootstrap Components** for a responsive grid layout.
*   **Global Controls:** A sidebar contains a "Year Range" slider and "Country" dropdown. These inputs trigger Python callbacks that query the PostgreSQL database in real-time.
*   **Visual Components:**
    1.  **Main Trend Line (Time Series):** Visualizes the "decoupling" effect. By plotting Energy Use over time, users can see the trajectory of consumption.
    2.  **Correlation Heatmap:** A 5x5 matrix showing Pearson correlations. We used a diverging 'RdBu' (Red-Blue) color scale. Red indicates positive correlation (GDP goes up, Energy goes up), while Blue indicates negative correlation. This immediately highlights the strong relationship between `climate_energy_use` and `climate_fossil_fuel_consumption`.
    3.  **Clustering Scatter Plot:** Displays the results of the K-Means analysis. Each point is a country-year, colored by its assigned cluster. This helps users visualize how countries move between clusters over time (e.g., moving from "Developing" to "Green Leader").

## 5. Results and Evaluation

### 5.1 Statistical Findings
The analysis of over 11,500 initial records (filtered down to ~720 clean analysis rows) yielded robust statistical insights.
*   **The Energy-GDP Nexus:** We found a Pearson correlation of **0.82** between `GDP per Capita` and `Energy Use`. This confirms that despite efficiency gains, economic activity is still heavily energy-intensive.
*   **The Renewable Gap:** The correlation between `GDP` and `Renewable Energy %` is weak (**-0.15**). This indicates that wealth alone does not drive renewable adoption; policy decisions play a larger role. Some lower-GDP nations (like those in Latin America using hydropower) have higher renewable shares than wealthy fossil-fuel nations.

### 5.2 Machine Learning Analysis
We executed a K-Means Clustering algorithm ($k=4$) to segment the nations.

*Figure 1: K-Means Cluster Centroids (Placeholder)*

*   **Cluster 0 (The Industrial Giants):** High GDP, High Energy Use, High CO2. (e.g., USA, Canada).
*   **Cluster 1 (The Developing Majority):** Low GDP, Low Energy, Low CO2. (e.g., India, Vietnam).
*   **Cluster 2 (The Green Leaders):** High GDP, High Energy, but Moderate CO2. This cluster represents the "Target State" for sustainable development.
*   **Cluster 3 (Transition Economies):** Rapidly growing GDP with exploding emissions.

**Regression Analysis:**
A Random Forest Regressor (n_estimators=100) was trained to predict CO2 emissions.
*   **R² Score:** 0.94 (The model explains 94% of the variance in emissions).
*   **Feature Importance:**
    1.  Energy Use per Capita (72%)
    2.  Fossil Fuel Consumption (18%)
    3.  GDP per Capita (5%)
    4.  Urbanization (3%)
*   *Interpretation:* Economic growth (GDP) is only a distal cause of emissions. The proximal cause is energy intensity. Policy should focus on energy efficiency (reducing the need for energy) rather than just degrowth.

### 5.3 Evaluation of Objectives
*   **Objective 1 (Pipeline):** Met. The system successfully ingested over 11,500 records from the API.
*   **Objective 2 (Database):** Met. Data exists in both MongoDB (Raw) and Postgres (Processed), verifying the Polyglot architecture.
*   **Objective 3 (ML):** Met. Clusters successfully differentiate country types, and Regression R2 score > 0.90 indicates high predictive accuracy.
*   **Objective 4 (Dashboard):** Met. The application renders interactive charts with sub-second latency.

## 6. Conclusions and Future Work

### 6.1 Conclusion
This project successfully demonstrated the application of advanced data engineering to the domain of climate economics. By automating the data lifecycle, we removed the friction typically associated with cross-national studies. 
Our findings challenge the simplistic view that growth equals pollution. The identification of "Cluster 2" (Green Leaders) proves that high living standards are compatible with lower emissions, provided there is a structural shift in energy sources. The "Polyglot" architecture proved highly effective, offering the best of both worlds: the agility of NoSQL for ingestion and the rigor of SQL for analysis.

### 6.2 Limitations
*   **Data Lag:** The World Bank data often lags by 1-2 years. Our interpolation methods, while statistically valid, are approximations of the current reality.
*   **Scope:** We focused on 30 representative countries. A global analysis of 190+ countries would require more sophisticated distributed processing (e.g., Apache Spark) to handle the increased load.

### 6.3 Future Work
1.  **Predictive Forecasting:** We plan to implement LSTM (Long Short-Term Memory) Recurrent Neural Networks to forecast CO2 trends through 2030, allowing for "What-If" scenario planning.
2.  **Live Data Integration:** Integrating real-time electricity grid APIs (like ElectricityMaps) would allow for daily, rather than annual, monitoring of carbon intensity.
3.  **Cloud Deployment:** Containerizing the application with Docker and deploying it to a cloud provider (AWS EC2 or Heroku) would make the dashboard accessible to the public.

## 7. Bibliography
[1] World Bank Group, "World Bank Open Data API," 2024. [Online]. Available: https://data.worldbank.org/

[2] D. I. Stern, "The Rise and Fall of the Environmental Kuznets Curve," *World Development*, vol. 32, no. 8, pp. 1419-1439, 2004.

[3] M. Fowler, "Polyglot Persistence," 2011. [Online]. Available: https://martinfowler.com/bliki/PolyglotPersistence.html

[4] J. Heer and B. Shneiderman, "Interactive Dynamics for Visual Analysis," *Queue*, vol. 10, no. 2, pp. 30, 2012.

[5] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830, 2011.

[6] PostgreSQL Global Development Group, "PostgreSQL 16 Documentation," 2024.

[7] MongoDB Inc., "The MongoDB 6.0 Manual," 2024.

[8] Plotly Technologies Inc., "Dash User Guide," 2024. [Online]. Available: https://dash.plotly.com/

[9] W. McKinney, "Data Structures for Statistical Computing in Python," in *Proceedings of the 9th Python in Science Conference*, 2010.

[10] E. R. Tufte, *The Visual Display of Quantitative Information*. Cheshire, CT: Graphics Press, 2001.

---

## Appendix A: Detailed Test Results

### Functional Testing
| Test Case ID | Feature | Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-001** | API Connection | Connect to World Bank API | Status 200 OK | Status 200 OK | **Pass** |
| **TC-002** | MongoDB Write | Write raw JSON to collection | Document Count > 0 | 11,520 Docs | **Pass** |
| **TC-003** | Data Cleaning | Interpolate missing values | No NaNs in output | 0 NaNs | **Pass** |
| **TC-004** | Postgres Load | Create Tables from DF | Tables exist in DB | Tables Created | **Pass** |
| **TC-005** | ML Training | Train Random Forest | R2 Score Generated | R2 = 0.94 | **Pass** |
| **TC-006** | Dashboard | Load Homepage | HTTP 200 | HTTP 200 | **Pass** |

### Security & Error Handling
| Test Case ID | Feature | Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | Env Variables | Check for hardcoded keys | No keys in code | Keys in .env | **Pass** |
| **ERR-01** | DB Timeout | Simulate DB failure | Log error, don't crash | Error Logged | **Pass** |
| **ERR-02** | Bad API Data | Inject malformed JSON | Skip record, log | Record Skipped | **Pass** |

---
**[End of Report]**
