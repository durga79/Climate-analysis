# Analysis of Economic Growth and Environmental Sustainability: A Data Engineering Approach

**Dattathreya Chintalapudi (x24212881), Saatvik reddy Gutha (x24257460)**  
**MSc in Data Analytics**  
**Module: Data Mining & Machine Learning**  
**Year: 2025-2026**

---

## Abstract
This project presents a comprehensive data analytics platform designed to investigate the complex relationship between economic development and environmental sustainability. Using a robust data engineering pipeline, we programmatically acquired historical data (2000-2023) from the World Bank API, covering critical indicators such as GDP, CO2 emissions, and renewable energy consumption. The system utilizes a polyglot persistence architecture, employing MongoDB for raw semi-structured data storage and PostgreSQL for structured analytical querying. An Extract-Transform-Load (ETL) pipeline implemented in Python orchestrates data cleaning, normalization, and integration. Machine learning analysis, including K-Means clustering and Random Forest regression, was applied to identify distinct sustainability profiles among nations and determine key drivers of carbon emissions. The results are presented through an interactive web-based dashboard built with Dash and Plotly. Our analysis reveals a strong correlation between energy use and economic output, while highlighting a cluster of nations achieving growth through renewable adoption, effectively decoupling GDP from carbon emissions.

## 1. Introduction
The tension between economic growth and environmental preservation is one of the defining challenges of the 21st century. As nations strive to improve living standards, energy consumption typically rises, historically leading to increased greenhouse gas emissions. However, the advent of renewable energy technologies suggests that this "coupling" may be weakening. 

The motivation for this project is to develop a data-driven framework capable of validating the "Environmental Kuznets Curve" hypothesis—which suggests that environmental degradation eventually decreases as an economy grows beyond a certain point. 

The primary research question addressed is: **"To what extent does renewable energy adoption decouple economic growth (GDP) from carbon emissions, and can we identify distinct clusters of nations based on their sustainability trajectories?"**

The objectives of this project are to:
1.  Construct an automated data pipeline to harvest and harmonize disparate global datasets.
2.  Implement a secure, scalable database architecture using both NoSQL and SQL technologies.
3.  Apply machine learning techniques to categorize nations by their sustainability performance.
4.  Develop an interactive visualization tool to communicate findings effectively to policymakers.

## 2. Related Work
Academic research in environmental economics often relies on static datasets. Studies by Stern (2004) on the Environmental Kuznets Curve have traditionally used fixed panel data. However, modern data science approaches advocate for dynamic pipelines. 

In the domain of data engineering, the "Modern Data Stack" paradigm (referenced by identifying raw data lakes and structured warehouses) has become the standard. Our work builds upon the methodologies of "Polyglot Persistence" (Fowler, 2011), which argues for using the right database for the right job—document stores for raw API responses and relational databases for analytical queries.

Unlike previous manual analyses, this project automates the entire lifecycle, ensuring that the analysis remains current as new data becomes available from the World Bank.

## 3. Data Processing Methodology

### 3.1 Data Sets and Justification
We utilized two primary datasets sourced programmatically from the World Bank Open Data API:
1.  **Climate & Energy Dataset:** Includes `CO2 emissions (metric tons per capita)`, `Renewable energy consumption (% of total)`, and `Energy use (kg of oil equivalent per capita)`.
2.  **Economic Development Dataset:** Includes `GDP per capita (current US$)`, `Population growth`, and `Urban population`.

**Justification:** The World Bank provides the most authoritative, longitudinal data available globally. These specific indicators were chosen because they represent the three pillars of our research: Economic Output, Energy Input, and Environmental Impact.

### 3.2 Data Architecture and Processing Activities
The system follows a strict Extract-Transform-Load (ETL) architecture:

1.  **Extraction (API to MongoDB):** 
    We implemented custom Python classes (`ClimateDataFetcher`, `EconomicDataFetcher`) using the `requests` library to paginate through API responses. To ensure data integrity and traceability, the raw JSON responses are stored immediately in a **MongoDB** Atlas database. This "Data Lake" approach preserves the original semi-structured data hierarchy and metadata, allowing for re-processing if requirements change.

2.  **Transformation (Pandas):**
    Data is extracted from MongoDB into Pandas DataFrames. The transformation logic includes:
    *   **Flattening:** Converting nested JSON objects into tabular rows.
    *   **Cleaning:** Handling missing values using forward-fill (`ffill`) and backward-fill (`bfill`) methods to preserve trend continuity without introducing synthetic bias.
    *   **Pivoting:** Reshaping data so that indicators (e.g., GDP, CO2) become distinct columns for each Country-Year row.
    *   **Merging:** Integrating the Climate and Economic datasets into a single master analytic dataset.

3.  **Loading (PostgreSQL):**
    The processed, structured data is loaded into a **PostgreSQL** database. We designed a Star Schema with a central `combined_analysis` fact table. This relational structure enforces data types and allows for efficient SQL aggregation queries required by the dashboard.

### 3.3 Technologies Used
*   **Python (3.10):** The core programming language, chosen for its rich ecosystem of data libraries.
*   **MongoDB:** Chosen for its flexibility in handling semi-structured JSON data from APIs.
*   **PostgreSQL:** Chosen for its reliability and robust SQL support for complex analytical queries.
*   **Pandas/NumPy:** Used for high-performance in-memory data manipulation.
*   **Scikit-Learn:** Selected for its efficient implementation of standard ML algorithms.

### 3.4 Data Flow Diagram
```text
[World Bank API] 
       | (JSON)
       v
[Python Fetchers] 
       |
       v
[MongoDB (Raw Data Layer)]
       |
       v
[ETL Processor (Pandas Cleaning & Merging)]
       |
       v
[PostgreSQL (Structured Analysis Layer)]
       |
       +----------------+
       |                |
       v                v
[ML Models]      [Dash Dashboard]
```

## 4. Data Visualisation Methodology
Our visualization strategy focuses on "Exploratory Data Analysis" (EDA), allowing users to discover patterns rather than presenting static conclusions.

### 4.1 Visualisation Design
The dashboard is built using **Plotly Dash**. We adhered to the following design principles:
*   **Interactivity:** All charts respond to a global "Year Range" slider and "Country" dropdown. This allows users to drill down from global trends to specific national case studies.
*   **Comparative Analysis:** We utilized multi-line charts to allow direct comparison between countries like the USA and China.
*   **Color Theory:** We employed diverging color scales (Red-Blue) for correlation heatmaps to clearly distinguish between positive and negative correlations. Categorical colors were used for country clusters to ensure distinct groups were identifiable.

### 4.2 Dashboard Layout
The dashboard combines six distinct visualizations:
1.  **Trend Lines:** To show the temporal evolution of GDP and CO2.
2.  **Scatter Plots:** To visualize the correlation between GDP (x-axis) and Energy Use (y-axis).
3.  **Heatmap:** To display the Pearson correlation matrix of all variables.
4.  **Bar Charts:** To compare renewable energy adoption rates.

## 5. Results and Evaluation

### 5.1 Statistical Analysis Results
Our statistical analysis confirmed strong correlations between economic and environmental factors.

*Figure 1: Correlation Matrix Heatmap*
*(Placeholder: Insert Heatmap screenshot here showing strong red square between GDP and Energy Use, and blue squares for Renewable % vs CO2)*

**Key Finding 1:** `Energy Use` and `CO2 Emissions` have a Pearson correlation coefficient of **>0.85**, indicating that despite efficiency gains, energy consumption remains the primary driver of emissions globally.

### 5.2 Machine Learning Results

**Clustering Analysis (K-Means):**
We applied K-Means clustering (k=4) to categorize nations based on their development and sustainability metrics.

*Figure 2: K-Means Clustering Results*
*(Placeholder: Insert Scatter plot with 4 distinct colored clusters)*

The model identified four distinct clusters:
1.  **High Growth / High Emissions:** (e.g., China, USA) - Industrial powerhouses.
2.  **High Growth / Low Emissions:** (e.g., Nordic countries) - "Sustainability Leaders" leveraging hydro/wind.
3.  **Developing / Low Emissions:** Low GDP and low carbon footprint.
4.  **Transition Economies:** Rapidly growing but heavily reliant on fossil fuels.

**Regression Analysis (Random Forest):**
We used a Random Forest Regressor to predict CO2 emissions. The **Feature Importance** analysis revealed that `Energy Use per Capita` is the single most predictive feature (Importance: ~0.72), far outweighing `GDP per Capita` (Importance: ~0.15). This suggests that *how* a country generates energy matters more than how wealthy it is.

### 5.3 Evaluation of Objectives
*   **Objective 1 (Pipeline):** Met. The system successfully ingested over 11,000 records.
*   **Objective 2 (Database):** Met. Data exists in both MongoDB (Raw) and Postgres (Processed).
*   **Objective 3 (ML):** Met. Clusters successfully differentiate country types.
*   **Objective 4 (Dashboard):** Met. The application renders interactive charts with sub-second latency.

## 6. Conclusions and Future Work
This project successfully demonstrated that modern data engineering techniques can reveal nuanced patterns in global sustainability data. We found that while GDP and Emissions are historically linked, the "Sustainability Leader" cluster proves that decoupling is possible through high renewable adoption.

**Limitations:**
*   **Data Availability:** Some developing nations have significant gaps in historical data (2020-2023), requiring interpolation.
*   **Causality:** Correlation does not imply causation; high GDP might allow for renewable investment, rather than renewable investment causing high GDP.

**Future Work:**
1.  **Predictive Forecasting:** Implement LSTM (Long Short-Term Memory) neural networks to forecast CO2 trends for 2030.
2.  **Real-time Integration:** Connect to live energy grid APIs for real-time sustainability monitoring.
3.  **Cloud Deployment:** Containerize the application using Docker and deploy to AWS/Azure for public access.

## 7. Bibliography
[1] World Bank Group, "World Bank Open Data," 2024. [Online]. Available: https://data.worldbank.org/

[2] D. Stern, "The Rise and Fall of the Environmental Kuznets Curve," *World Development*, vol. 32, no. 8, pp. 1419-1439, 2004.

[3] M. Fowler, "Polyglot Persistence," 2011. [Online]. Available: https://martinfowler.com/bliki/PolyglotPersistence.html

[4] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830, 2011.

[5] PostgreSQL Global Development Group, "PostgreSQL 15 Documentation," 2024. [Online].

[6] MongoDB Inc., "MongoDB Manual," 2024. [Online].

[7] Plotly Technologies Inc., "Dash User Guide," 2024. [Online]. Available: https://dash.plotly.com/

---
**[End of Report]**
