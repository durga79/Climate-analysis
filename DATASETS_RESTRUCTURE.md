# Dataset Restructuring: 3 → 2 Datasets

## Original Structure (3 Datasets):
1. Climate Data (1,440 records)
2. Economic Data (5,760 records)
3. Renewable Energy Data (4,320 records)

## New Structure (2 Datasets for Team of 2):

### Dataset 1: Climate & Energy Data (Combined)
- **Source:** World Bank API
- **Format:** JSON (semi-structured)
- **Original Collections:** 
  - climate_data_raw (1,440 docs)
  - renewable_data_raw (4,320 docs)
- **Combined Records:** 5,760 documents
- **Indicators:** 12 total
  - Energy use per capita
  - Fossil fuel consumption %
  - Renewable energy consumption %
  - Renewable electricity output %
  - Electricity production from renewables
  - Alternative/nuclear energy %
  - Combustible renewables & waste %
  - Electric power consumption
- **Justification:** Climate and renewable energy are intrinsically linked - renewable energy is a key climate solution

### Dataset 2: Economic Development Data
- **Source:** World Bank API
- **Format:** JSON (semi-structured)
- **Collection:** economic_data_raw (5,760 docs)
- **Indicators:** 8 total
  - GDP (current USD)
  - GDP per capita
  - GDP growth rate
  - Population
  - Urban population %
  - Industry value added %
  - Services value added %
  - Exports of goods & services %
- **Justification:** Economic development indicators to analyze relationship with environmental sustainability

## Research Question (Updated):
"How does economic development correlate with energy consumption and renewable energy adoption across countries from 2000-2023?"

## Key Points:
- **2 datasets** (perfect for team of 2)
- **Both semi-structured** (JSON from API)
- **Combined: 11,520 raw records** (exceeds 1,000 minimum)
- **30 countries, 24 years**
- **After ETL: 720 processed records** in combined_analysis table

This structure is actually better for your analysis as it creates a clear separation:
- Dataset 1: Environmental/Energy (what's happening to environment)
- Dataset 2: Economic (what's happening with development)
