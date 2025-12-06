# Dataset Description - 2 Datasets for Team of 2

## Overview
This project uses **two comprehensive datasets** from the World Bank API, structured for a team of 2 members. Both datasets are in semi-structured JSON format retrieved programmatically via API.

---

## Dataset 1: Climate & Energy Data (Member 1)

### Source
- **API:** World Bank API v2
- **Base URL:** `https://api.worldbank.org/v2/`
- **Format:** JSON (semi-structured)
- **Retrieval Method:** Programmatic API calls using Python `requests` library

### Coverage
- **Countries:** 30 countries across all continents
- **Time Period:** 2000-2023 (24 years)
- **Total Records:** ~5,760 documents (combined from climate_data_raw + renewable_data_raw)
- **Storage:** MongoDB collections: `climate_data_raw` + `renewable_data_raw`

### Indicators (12 total)

**Climate/Energy Indicators:**
1. `climate_energy_use` - Energy use (kg of oil equivalent per capita)
2. `climate_fossil_fuel_consumption` - Fossil fuel energy consumption (% of total)

**Renewable Energy Indicators:**
3. `renewable_renewable_energy_consumption_pct` - Renewable energy consumption (% of total)
4. `renewable_renewable_electricity_output_pct` - Renewable electricity output (%)
5. `renewable_electricity_production_renewable` - Electricity production from renewable sources
6. `renewable_alternative_nuclear_energy_pct` - Alternative and nuclear energy (%)
7. `renewable_combustible_renewables_waste_pct` - Combustible renewables and waste (%)
8. `renewable_electric_power_consumption_kwh` - Electric power consumption (kWh per capita)

### Justification
Climate and renewable energy data are combined into a single dataset because they are intrinsically linked:
- Renewable energy is a direct solution to climate/energy challenges
- Understanding energy patterns requires analyzing both conventional and renewable sources
- This grouping allows comprehensive environmental/energy analysis

### Data Quality
- **Completeness:** ~95% of records have valid data
- **Missing Values:** Handled through forward/backward fill methods
- **Validation:** Year range 2000-2023, all country codes are valid 3-letter ISO codes

---

## Dataset 2: Economic Development Data (Member 2)

### Source
- **API:** World Bank API v2
- **Base URL:** `https://api.worldbank.org/v2/`
- **Format:** JSON (semi-structured)
- **Retrieval Method:** Programmatic API calls using Python `requests` library

### Coverage
- **Countries:** 30 countries across all continents
- **Time Period:** 2000-2023 (24 years)
- **Total Records:** ~5,760 documents
- **Storage:** MongoDB collection: `economic_data_raw`

### Indicators (8 total)

1. `economic_gdp_current_usd` - GDP (current US$)
2. `economic_gdp_per_capita` - GDP per capita (current US$)
3. `economic_gdp_growth` - GDP growth (annual %)
4. `economic_population` - Total population
5. `economic_urban_population_pct` - Urban population (% of total)
6. `economic_industry_value_added_pct` - Industry value added (% of GDP)
7. `economic_services_value_added_pct` - Services value added (% of GDP)
8. `economic_exports_goods_services_pct` - Exports of goods and services (% of GDP)

### Justification
Economic development indicators are essential for:
- Understanding the relationship between economic growth and environmental sustainability
- Analyzing how wealth affects energy consumption patterns
- Identifying whether sustainable development is possible

### Data Quality
- **Completeness:** ~98% of records have valid data
- **Missing Values:** Handled through interpolation methods
- **Validation:** All numeric values are positive, year range validated

---

## Combined Dataset Analysis

### After ETL Processing
- **PostgreSQL Table:** `combined_analysis`
- **Merged Records:** 720 rows
- **Merge Key:** (year, country_code)
- **Total Columns:** 21 columns
  - 3 metadata (year, country_code, country_name)
  - 12 from Dataset 1 (Climate & Energy)
  - 8 from Dataset 2 (Economic)
  - 2 derived features (categories)

### Countries Included (30 total)
ARG, AUS, BEL, BRA, CAN, CHL, CHN, DEU, DNK, ESP, FIN, FRA, GBR, IDN, IND, ITA, JPN, KOR, MEX, NLD, NOR, NZL, POL, RUS, SAU, SGP, SWE, TUR, USA, ZAF

### Data Processing Pipeline

**Step 1: Acquisition**
- Fetch JSON data from World Bank API
- Store raw data in MongoDB (2 logical datasets, 3 collections)

**Step 2: ETL**
- Extract from MongoDB
- Clean and transform (handle missing values, remove duplicates)
- Merge on (year, country_code)
- Load to PostgreSQL

**Step 3: Analysis**
- Statistical analysis (correlations, trends)
- Machine learning (regression, clustering)
- Visualization (interactive dashboard)

---

## Research Questions Addressed

### Primary Research Question
"How does economic development correlate with energy consumption and renewable energy adoption across countries from 2000-2023?"

### Sub-Questions
1. Is there a relationship between GDP per capita and energy use?
2. Do wealthier countries adopt more renewable energy?
3. What patterns distinguish sustainable development leaders?
4. Has renewable energy adoption increased over time globally?

---

## Data Strengths

1. **Official Source:** World Bank provides authoritative, standardized data
2. **Comprehensive Coverage:** 30 countries, 24 years, 20 indicators
3. **Temporal Analysis:** Long time period allows trend analysis
4. **Semi-structured:** JSON format meets assignment requirements
5. **Programmatic:** All data retrieved via API (not manual downloads)
6. **Large Volume:** 11,520 raw records exceeds 1,000 minimum requirement

---

## Data Limitations

1. **API Availability:** Some CO2 indicators were not available from the API
2. **Missing Values:** Some countries missing data for certain years (~5-10%)
3. **Time Lag:** Most recent data may be 1-2 years behind current year
4. **Developed Country Bias:** Better data quality for developed nations

---

## Assignment Compliance

| Requirement | Specification | Our Implementation | Status |
|------------|---------------|-------------------|--------|
| **Number of datasets** | 1 per team member (team of 2) | 2 datasets | ✅ |
| **Semi-structured** | At least 1 dataset | Both are JSON | ✅ |
| **Record count** | Min 1,000 per dataset | 5,760 each | ✅ |
| **Programmatic retrieval** | API or web scraping | World Bank API | ✅ |
| **Database storage (before)** | Required | MongoDB | ✅ |
| **Database storage (after)** | Required | PostgreSQL | ✅ |

---

## Technical Implementation

### Data Acquisition
- **Language:** Python 3.10+
- **Libraries:** `requests`, `pymongo`, `pandas`
- **Retry Logic:** Exponential backoff for API failures
- **Rate Limiting:** Respectful delays between API calls

### Storage
- **MongoDB:** NoSQL database for raw semi-structured JSON
- **PostgreSQL:** Relational database for processed structured data
- **Cloud Deployment:** MongoDB Atlas + Neon.tech PostgreSQL

### Processing
- **ETL Pipeline:** Complete Extract-Transform-Load
- **Data Cleaning:** Handle missing values, remove duplicates
- **Validation:** Type checking, range validation, integrity checks

---

## Summary

This project successfully implements a **2-dataset structure** perfectly suited for a team of 2:
- **Dataset 1:** Climate & Energy (environmental perspective)
- **Dataset 2:** Economic Development (economic perspective)

Both datasets are semi-structured JSON from the World Bank API, each containing 5,760+ records, and together enable comprehensive analysis of the relationship between economic development and environmental sustainability.

