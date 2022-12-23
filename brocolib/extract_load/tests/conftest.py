import pytest
import pandas as pd


## ----------| DATA |----------

## -----| pandas.DataFrame |-----

@pytest.fixture
def get_dummy_df():
    return pd.DataFrame([
  {'Scoville' : 50, 'Name' : 'Bell pepper', 'Feeling' : 'Not even spicy'},
  {'Scoville' : 5000, 'Name' : 'Espelette pepper', 'Feeling' : 'Uncomfortable'},
  {'Scoville' : 500000, 'Name' : 'Chocolate habanero', 'Feeling' : 'Practically ate pepper spray'},
])

@pytest.fixture
def get_empty_df():
    return pd.DataFrame()
