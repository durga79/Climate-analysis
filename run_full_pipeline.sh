#!/bin/bash

echo "================================================================================"
echo "CLIMATE ANALYTICS PROJECT - FULL PIPELINE EXECUTION"
echo "================================================================================"
echo ""

set -e

echo "[STEP 1/5] Data Acquisition from World Bank API..."
echo "--------------------------------------------------------------------------------"
cd src/data_acquisition
python fetch_all_datasets.py
cd ../..
echo "✓ Data acquisition completed"
echo ""

echo "[STEP 2/5] ETL Pipeline - Extract, Transform, Load..."
echo "--------------------------------------------------------------------------------"
cd src/etl
python pipeline.py
cd ../..
echo "✓ ETL pipeline completed"
echo ""

echo "[STEP 3/5] Statistical Analysis..."
echo "--------------------------------------------------------------------------------"
cd src/analysis
python statistical_analysis.py
cd ../..
echo "✓ Statistical analysis completed"
echo ""

echo "[STEP 4/5] Machine Learning Analysis..."
echo "--------------------------------------------------------------------------------"
cd src/analysis
python ml_models.py
cd ../..
echo "✓ Machine learning analysis completed"
echo ""

echo "[STEP 5/5] Launching Dashboard..."
echo "--------------------------------------------------------------------------------"
echo "Dashboard will be available at: http://localhost:8050"
echo "Press Ctrl+C to stop the dashboard"
echo ""
cd dashboard
python app.py


