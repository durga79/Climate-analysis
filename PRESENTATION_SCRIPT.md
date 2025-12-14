# 10-Minute Video Presentation Script
**Project:** Climate Analytics & Economic Development
**Presenters:** Dattathreya Chintalapudi & Saatvik reddy Gutha

---

## 0:00 - 1:30 | Introduction (Dattathreya)

**Dattathreya:**
"Hello everyone. My name is Dattathreya, and together with my teammate Saatvik, we are presenting our project: **'Analysis of Economic Growth and Environmental Sustainability: A Data Engineering Approach'**.

The motivation for this project stems from the 'Green Growth Paradox'. We live in a world where economic development—measured by GDP—has historically been tied to carbon emissions. We wanted to answer a critical research question: **'Can nations continue to grow their economies while reducing their carbon footprint through renewable energy?'**

To answer this, we built a complete, end-to-end data pipeline. Instead of just downloading a CSV file, we wanted to demonstrate a production-grade 'Modern Data Stack'. We ingested over 11,000 live records from the World Bank API, processed them using a Polyglot Persistence architecture, and applied Machine Learning to find the answer.

I will now walk you through the Data Engineering architecture that powers this system."

---

## 1:30 - 4:30 | Data Engineering & Architecture (Dattathreya)

**Dattathreya:**
"My primary role was **Data Engineering and Backend Infrastructure**.

**1. Data Acquisition Strategy:**
I built a Python-based ingestion engine. The World Bank API is complex—it uses pagination and nested JSON. I wrote a custom `ClimateDataFetcher` class that recursively loops through pages to ensure we don't miss a single year of data from 2000 to 2023. I also implemented an 'Exponential Backoff' algorithm. If the API fails or times out, our system automatically waits and retries, making the pipeline highly resilient.

**2. The Polyglot Database Architecture:**
We didn't just use one database; we used the right tool for the job.
*   **MongoDB (The Data Lake):** I set up a MongoDB Atlas cluster to store the raw, semi-structured JSON exactly as it came from the API. This ensures we have a 'pristine' backup of the source truth.
*   **PostgreSQL (The Data Warehouse):** For the analytics layer, I deployed a PostgreSQL database.

**3. The ETL Pipeline:**
I developed the Extract-Transform-Load pipeline in Python. The challenge here was dirty data. Indicators like CO2 often lag by 2-3 years. I implemented a time-series interpolation strategy—using Forward Fill and Backward Fill—to intelligently estimate missing values so our Machine Learning models wouldn't crash.

Once the data was clean and structured, it was handed off to the analytics layer. I'll pass it over to Saatvik to discuss the insights."

---

## 4:30 - 7:30 | Analytics, ML & Visualization (Saatvik)

**Saatvik:**
"Thanks, Dattathreya. My focus was on **Data Analytics, Machine Learning, and Visualization**.

**1. Machine Learning Analysis:**
Once we had the clean data, I applied two specific algorithms to answer our research question.
*   First, I used **K-Means Clustering**. By grouping countries based on GDP and Renewable adoption, we identified four distinct clusters. Most interestingly, we found a 'Green Leader' cluster—countries with High GDP but Low Emissions—proving that decoupling is possible.
*   Second, I trained a **Random Forest Regressor** to predict CO2 emissions. The model achieved an accuracy ($R^2$) of 94%. Crucially, the Feature Importance analysis showed that **Energy Use** is the #1 driver of emissions (72%), far outweighing GDP (5%). This suggests policy should focus on energy efficiency, not just economic degrowth.

**2. Interactive Dashboard:**
To make these findings accessible, I built a web-based dashboard using **Plotly Dash**.
*   It's not static; it's fully interactive. Users can filter by any Country or Year range.
*   I implemented complex Python callbacks that update all charts simultaneously.
*   You can see the Correlation Heatmap here [Show Slide/Demo], which visualizes the strong link between Fossil Fuels and Emissions (Red blocks), compared to the negative correlation with Renewables (Blue blocks).

This dashboard allows policymakers to explore the data dynamically rather than reading a static report."

---

## 7:30 - 9:00 | Challenges & Evaluation (Joint)

**Saatvik:**
"We faced several technical challenges. For instance, generating static images for our report using the Kaleido engine caused version conflicts, which we solved by debugging the dependency tree together."

**Dattathreya:**
"On the backend, a major challenge was module imports. As our project grew into nested folders (`src/etl`, `src/analysis`), Python couldn't find our config files. I implemented a programmatic `sys.path` injection fix to ensure our scripts run reliably on any machine, Windows or Linux."

**Saatvik:**
"In terms of evaluation, we met all project objectives. We have a Polyglot database, a reproducibe ETL pipeline, and statistically significant ML results."

---

## 9:00 - 10:00 | Conclusion (Joint)

**Dattathreya:**
"To conclude, this project demonstrates that Modern Data Engineering is essential for climate science. By automating the data lifecycle, we can spend less time cleaning data and more time finding solutions."

**Saatvik:**
"Our analysis proves that while economic growth historically drives emissions, renewable technology offers a clear path to sustainability. Thank you for listening."

**Both:**
"Thank you."

