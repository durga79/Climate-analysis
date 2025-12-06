# Setup Guide - Climate Analytics Project

This guide provides step-by-step instructions to set up and run the complete analytics pipeline.

## Prerequisites

- Python 3.11 or higher
- MongoDB 6.0+
- PostgreSQL 14+
- pip or virtualenv

## Installation Steps

### 1. Clone/Extract Project

```bash
cd /home/durga/climate-analytics-project
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### MongoDB Setup

```bash
# Start MongoDB service
sudo systemctl start mongod

# Or if using Docker:
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Verify connection
mongosh
```

#### PostgreSQL Setup

```bash
# Create database
sudo -u postgres psql
CREATE DATABASE climate_analytics;
CREATE USER analytics_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE climate_analytics TO analytics_user;
\q

# Or using command line:
createdb climate_analytics
```

### 5. Environment Configuration

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Update the following:
```
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=climate_analytics
POSTGRES_URI=postgresql://analytics_user:your_password@localhost:5432/climate_analytics
WORLD_BANK_API_BASE=https://api.worldbank.org/v2/
```

## Running the Pipeline

### Step 1: Data Acquisition

```bash
cd src/data_acquisition
python fetch_all_datasets.py
```

**Expected Output:**
- Climate data records: ~4000+
- Economic data records: ~5000+
- Renewable data records: ~3500+
- All stored in MongoDB

**Time:** ~10-15 minutes depending on API response

### Step 2: ETL Pipeline

```bash
cd ../etl
python pipeline.py
```

**Expected Output:**
- Data extracted from MongoDB
- Transformed and cleaned
- Loaded into PostgreSQL tables

**Time:** ~2-5 minutes

### Step 3: Run Analysis

```bash
cd ../analysis

# Statistical analysis
python statistical_analysis.py

# Machine learning models
python ml_models.py
```

**Expected Output:**
- Correlation matrices
- Regression model results
- Clustering results
- Sustainability rankings

**Time:** ~3-5 minutes

### Step 4: Launch Dashboard

```bash
cd ../../dashboard
python app.py
```

**Access Dashboard:**
- Open browser to: http://localhost:8050
- Interactive visualizations will be available

### Step 5: Explore with Jupyter Notebooks

```bash
cd ../notebooks
jupyter notebook
```

Open and run:
- `01_data_acquisition.ipynb`
- `02_data_exploration.ipynb`

## Verification Checklist

### MongoDB Verification

```bash
mongosh
use climate_analytics
show collections
db.climate_data_raw.countDocuments()
db.economic_data_raw.countDocuments()
db.renewable_data_raw.countDocuments()
```

### PostgreSQL Verification

```bash
psql climate_analytics
\dt
SELECT COUNT(*) FROM combined_analysis;
SELECT COUNT(*) FROM climate_indicators;
SELECT COUNT(*) FROM economic_indicators;
SELECT COUNT(*) FROM renewable_energy;
\q
```

## Troubleshooting

### Issue: MongoDB Connection Failed

**Solution:**
```bash
sudo systemctl status mongod
sudo systemctl restart mongod
```

### Issue: PostgreSQL Connection Failed

**Solution:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Reset password if needed
sudo -u postgres psql
ALTER USER analytics_user WITH PASSWORD 'new_password';
```

### Issue: API Rate Limiting

**Solution:**
- The scripts include retry logic with exponential backoff
- If persistent, reduce the number of countries in the fetcher scripts

### Issue: Missing Python Packages

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: Dashboard Not Loading Data

**Solution:**
```bash
# Ensure PostgreSQL has data
psql climate_analytics -c "SELECT COUNT(*) FROM combined_analysis;"

# Check database connection in .env
cat .env | grep POSTGRES_URI

# Restart dashboard
python dashboard/app.py
```

## Performance Optimization

### For Large Datasets

If processing larger country sets or longer time ranges:

1. **MongoDB Indexing:**
```javascript
use climate_analytics
db.climate_data_raw.createIndex({"countryiso3code": 1, "date": 1})
db.economic_data_raw.createIndex({"countryiso3code": 1, "date": 1})
db.renewable_data_raw.createIndex({"countryiso3code": 1, "date": 1})
```

2. **PostgreSQL Indexing:**
```sql
CREATE INDEX idx_combined_country_year ON combined_analysis(country_code, year);
CREATE INDEX idx_climate_country_year ON climate_indicators(country_code, year);
```

## Development Workflow

### Adding New Countries

Edit the country list in:
- `src/data_acquisition/fetch_climate_data.py`
- `src/data_acquisition/fetch_economic_data.py`
- `src/data_acquisition/fetch_renewable_data.py`

Then rerun the acquisition scripts.

### Adding New Indicators

1. Find indicator code on World Bank website
2. Add to `indicators` dictionary in fetcher scripts
3. Rerun data acquisition
4. Update transform.py to handle new columns

## Testing

```bash
cd tests
pytest test_data_quality.py
pytest test_transformations.py
```

## Backup and Export

### Export PostgreSQL Data

```bash
pg_dump climate_analytics > backup.sql
```

### Export MongoDB Data

```bash
mongodump --db climate_analytics --out backup/
```

## Production Deployment

For production deployment:

1. Update `.env` with production credentials
2. Use production-grade MongoDB (Atlas) and PostgreSQL (RDS/Cloud SQL)
3. Deploy dashboard using Gunicorn:
```bash
gunicorn dashboard.app:server -b 0.0.0.0:8050
```

## Support

For issues or questions:
- Check logs in console output
- Review MongoDB/PostgreSQL logs
- Ensure all prerequisites are installed
- Verify .env configuration

## Next Steps

After successful setup:
1. Explore the dashboard visualizations
2. Run Jupyter notebooks for detailed analysis
3. Review the generated results
4. Customize analysis for your specific research questions


