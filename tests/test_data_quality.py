import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.postgres_handler import PostgresHandler
import pandas as pd

@pytest.fixture
def postgres_handler():
    handler = PostgresHandler()
    if handler.connect():
        yield handler
        handler.disconnect()
    else:
        pytest.skip("PostgreSQL connection not available")

def test_combined_analysis_table_exists(postgres_handler):
    tables = postgres_handler.get_table_names()
    assert 'combined_analysis' in tables, "combined_analysis table should exist"

def test_minimum_record_count(postgres_handler):
    df = postgres_handler.read_table('combined_analysis')
    assert len(df) >= 500, "Should have at least 500 records"

def test_required_columns_present(postgres_handler):
    df = postgres_handler.read_table('combined_analysis')
    required_columns = ['year', 'country_code', 'country_name']
    
    for col in required_columns:
        assert col in df.columns, f"Column {col} should be present"

def test_no_duplicate_country_year(postgres_handler):
    df = postgres_handler.read_table('combined_analysis')
    duplicates = df.duplicated(subset=['year', 'country_code']).sum()
    assert duplicates == 0, "Should not have duplicate (year, country_code) combinations"

def test_year_range_validity(postgres_handler):
    df = postgres_handler.read_table('combined_analysis')
    assert df['year'].min() >= 2000, "Minimum year should be >= 2000"
    assert df['year'].max() <= 2025, "Maximum year should be <= 2025"

def test_numeric_columns_validity(postgres_handler):
    df = postgres_handler.read_table('combined_analysis')
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    for col in numeric_cols:
        assert not df[col].isnull().all(), f"{col} should have some non-null values"

def test_country_code_format(postgres_handler):
    df = postgres_handler.read_table('combined_analysis')
    invalid_codes = df[df['country_code'].str.len() != 3]
    assert len(invalid_codes) == 0, "All country codes should be 3 characters"


