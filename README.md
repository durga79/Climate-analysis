# Climate Analytics & Economic Development Project

## Research Question
How do CO2 emissions and renewable energy adoption correlate with economic development indicators across countries from 2000-2023, and what patterns distinguish high-performing sustainability leaders?

## Project Overview
This project analyzes the relationship between environmental sustainability metrics and economic development across multiple countries, utilizing comprehensive datasets from international organizations.

## Datasets
1. **World Bank Climate Data** (JSON) - CO2 emissions, energy consumption
2. **World Bank Economic Indicators** (JSON) - GDP, GDP per capita, growth rates  
3. **IRENA Renewable Energy Data** (JSON/XML) - Renewable energy capacity and adoption

## Technology Stack
- **Language**: Python 3.11+
- **Databases**: MongoDB (semi-structured), PostgreSQL (structured)
- **Visualization**: Plotly + Dash
- **Analysis**: pandas, scikit-learn, scipy

## Project Structure
```
climate-analytics-project/
├── data/               # Raw and processed data
├── notebooks/          # Jupyter notebooks for exploration
├── src/               # Source code
├── dashboard/         # Dash application
├── tests/             # Unit tests
├── docs/              # Documentation and reports
└── config/            # Configuration files
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# MongoDB (ensure MongoDB is running)
mongod --dbpath /path/to/data

# PostgreSQL (create database)
createdb climate_analytics
```

### 3. Configure Environment
Create a `.env` file with:
```
MONGODB_URI=mongodb://localhost:27017/
POSTGRES_URI=postgresql://user:password@localhost:5432/climate_analytics
WORLD_BANK_API_BASE=https://api.worldbank.org/v2/
```

### 4. Run Data Pipeline
```bash
# Acquire data
python src/data_acquisition/fetch_all_datasets.py

# Run ETL
python src/etl/pipeline.py

# Run analysis
python src/analysis/run_analysis.py
```

### 5. Launch Dashboard
```bash
python dashboard/app.py
```

## Team Members
- [Student Name] - [Student Number]
- [Student Name] - [Student Number]
- [Student Name] - [Student Number]

## License
Academic Project - NCI 2024/25


