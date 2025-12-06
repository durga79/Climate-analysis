# Dataset Description

## Overview

This project utilizes three complementary datasets from the World Bank API, covering 30 countries from 2000-2023.

## Dataset 1: Climate Indicators

**Source:** World Bank Climate Change API  
**Format:** JSON (Semi-structured)  
**API Endpoint:** `https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}`

### Indicators Collected:

| Indicator | Code | Description | Unit |
|-----------|------|-------------|------|
| CO2 Emissions | EN.ATM.CO2E.KT | Total CO2 emissions | Kilotons |
| CO2 per Capita | EN.ATM.CO2E.PC | CO2 emissions per person | Metric tons per capita |
| Energy Use | EG.USE.PCAP.KG.OE | Energy use per capita | kg of oil equivalent |
| Fossil Fuel Consumption | EG.USE.COMM.FO.ZS | Fossil fuel energy consumption | % of total |
| Methane Emissions | EN.ATM.METH.KT.CE | Methane emissions | kt of CO2 equivalent |
| Nitrous Oxide Emissions | EN.ATM.NOXE.KT.CE | Nitrous oxide emissions | kt of CO2 equivalent |

### Data Characteristics:
- **Records:** ~4,000+ (6 indicators × 30 countries × 24 years, with some missing)
- **Time Range:** 2000-2023
- **Structure:** Nested JSON with country and indicator metadata
- **Quality:** Official reported statistics, some gaps for recent years

### Sample JSON Structure:
```json
{
  "indicator": {"id": "EN.ATM.CO2E.KT", "value": "CO2 emissions (kt)"},
  "country": {"id": "USA", "value": "United States"},
  "countryiso3code": "USA",
  "date": "2020",
  "value": 4713167.2,
  "unit": "",
  "obs_status": "",
  "decimal": 1
}
```

---

## Dataset 2: Economic Indicators

**Source:** World Bank Development Indicators API  
**Format:** JSON (Semi-structured)  
**API Endpoint:** `https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}`

### Indicators Collected:

| Indicator | Code | Description | Unit |
|-----------|------|-------------|------|
| GDP Current USD | NY.GDP.MKTP.CD | Gross Domestic Product | Current US$ |
| GDP per Capita | NY.GDP.PCAP.CD | GDP divided by population | Current US$ |
| GDP Growth | NY.GDP.MKTP.KD.ZG | Annual GDP growth rate | % |
| Population | SP.POP.TOTL | Total population | People |
| Urban Population % | SP.URB.TOTL.IN.ZS | Urban population | % of total |
| Industry Value Added % | NV.IND.TOTL.ZS | Industry value added | % of GDP |
| Services Value Added % | NV.SRV.TOTL.ZS | Services value added | % of GDP |
| Exports % | NE.EXP.GNFS.ZS | Exports of goods/services | % of GDP |

### Data Characteristics:
- **Records:** ~5,500+ (8 indicators × 30 countries × 24 years)
- **Time Range:** 2000-2023
- **Structure:** Identical JSON format to climate data
- **Quality:** High-quality macroeconomic data with minimal gaps

### Economic Development Context:
- Enables correlation analysis between economy and environment
- GDP per capita serves as proxy for development level
- Industry/services split indicates economic structure

---

## Dataset 3: Renewable Energy Indicators

**Source:** World Bank Energy API  
**Format:** JSON (Semi-structured)  
**API Endpoint:** `https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}`

### Indicators Collected:

| Indicator | Code | Description | Unit |
|-----------|------|-------------|------|
| Renewable Energy Consumption % | EG.FEC.RNEW.ZS | Renewable energy consumption | % of total |
| Renewable Electricity Output % | EG.ELC.RNEW.ZS | Renewable electricity output | % of total |
| Alternative/Nuclear Energy % | EG.USE.COMM.CL.ZS | Alternative and nuclear energy | % |
| Renewable Electricity Production | EG.ELC.RNWX.KH | Renewable electricity output | Billion kWh |
| Combustible Renewables/Waste % | EG.USE.CRNW.ZS | Combustible renewables and waste | % of total |
| Electric Power Consumption | EG.USE.ELEC.KH.PC | Electric power consumption | kWh per capita |

### Data Characteristics:
- **Records:** ~3,800+ (6 indicators × 30 countries × 24 years)
- **Time Range:** 2000-2023
- **Structure:** JSON format consistent with other datasets
- **Quality:** Good coverage, increasing data availability in recent years

### Renewable Energy Context:
- Tracks energy transition progress
- Renewable % is key metric for sustainability
- Complements fossil fuel data from climate dataset

---

## Country Coverage (30 Countries)

### Developed Economies:
- **North America:** USA, CAN
- **Europe:** DEU, GBR, FRA, ITA, ESP, NLD, BEL, SWE, NOR, DNK, FIN, POL
- **Asia-Pacific:** JPN, AUS, NZL, SGP, KOR

### Emerging Economies:
- **Asia:** CHN, IND, IDN
- **Latin America:** BRA, MEX, ARG, CHL
- **Middle East:** SAU, TUR
- **Africa:** ZAF
- **Europe:** RUS

### Selection Rationale:
- Mix of developed and developing nations
- Major emitters included (USA, CHN, IND)
- Renewable leaders included (NOR, SWE, DNK)
- Geographic diversity
- Data availability and quality

---

## Data Integration Strategy

### MongoDB Storage (Raw Data):
```
Collections:
├── climate_data_raw      (~4,000 documents)
├── economic_data_raw     (~5,500 documents)
└── renewable_data_raw    (~3,800 documents)

Total: ~13,300 raw records
```

### PostgreSQL Storage (Processed Data):
```
Tables:
├── countries             (30 rows - reference table)
├── climate_indicators    (~2,800 rows after cleaning)
├── economic_indicators   (~4,200 rows after cleaning)
├── renewable_energy      (~3,000 rows after cleaning)
└── combined_analysis     (~2,500 rows - merged data)
```

### Data Reduction After ETL:
- **Raw Records:** 13,300
- **After Cleaning:** ~10,000 (remove nulls, duplicates)
- **After Merging:** ~2,500 (inner join on year+country with all data)

---

## Data Quality Considerations

### Missing Data Patterns:
1. **Recent Years (2021-2023):** Some indicators lag 1-2 years
2. **Developing Countries:** More gaps in historical data
3. **Specific Indicators:** Methane/nitrous oxide less complete

### Handling Strategy:
- **Forward/Backward Fill:** Within same country time series
- **Threshold:** Drop rows missing >50% of columns
- **Imputation:** NOT used (maintains data integrity)

### Data Validation:
- Country codes validated (ISO 3-letter codes)
- Year range checked (2000-2023)
- Numeric ranges validated (no negative GDP, etc.)
- Duplicate detection on (country, year, indicator)

---

## Compliance with Project Requirements

### Requirement Checklist:
✅ **Minimum 3 datasets** (Climate, Economic, Renewable)  
✅ **At least 1000 records** (13,300 raw, 2,500+ processed)  
✅ **Semi-structured data** (JSON from API)  
✅ **Programmatic retrieval** (Python scripts with API calls)  
✅ **MongoDB storage** (before processing)  
✅ **PostgreSQL storage** (after processing)  
✅ **ETL pipeline** (Extract → Transform → Load)

### Data Justification:
This dataset combination enables answering the research question:
> "How do CO2 emissions and renewable energy adoption correlate with economic development indicators?"

- **Climate data** provides dependent variables (CO2, emissions)
- **Economic data** provides independent variables (GDP, development)
- **Renewable data** provides transition metrics (energy shift)

---

## Dataset Limitations

### Temporal:
- Data availability decreases for recent years
- Historical data (pre-2000) not included
- Annual granularity (no monthly/quarterly data)

### Geographic:
- National-level aggregation (no sub-national data)
- Country selection biased toward larger economies
- Small island nations underrepresented

### Measurement:
- Self-reported national statistics (accuracy varies)
- Methodological changes over time
- Different measurement standards across countries

### Scope:
- Focuses on production-based emissions (not consumption-based)
- Doesn't capture carbon sequestration/offsets
- Limited sectoral breakdown

---

## Data Access and Reproducibility

### API Access:
- **No authentication required** for World Bank API
- **Rate limits:** Reasonable (not documented, but generous)
- **Availability:** Public, free, maintained by World Bank
- **Documentation:** https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

### Reproducibility:
All data can be re-fetched by running:
```bash
python src/data_acquisition/fetch_all_datasets.py
```

No manual downloads required. Complete programmatic pipeline.

---

## References

1. World Bank. (2024). *World Development Indicators*. Retrieved from https://databank.worldbank.org/

2. World Bank. (2024). *Climate Change Data*. Retrieved from https://data.worldbank.org/topic/climate-change

3. World Bank. (2024). *Energy & Mining Data*. Retrieved from https://data.worldbank.org/topic/energy-and-mining


