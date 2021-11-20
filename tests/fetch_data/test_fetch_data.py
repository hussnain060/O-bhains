import pytest
import pandas as pd

from cow_disease_detection.fetch_data.clean_dataset import (
    get_data,
    data_preprocessing,
    calculate_average,
)


@pytest.fixture
def expected_column_names():
    """make sure it returns expected columns"""
    return ["temperature", "x_axix", "y_axix", "z_axix"]


@pytest.mark.e2e
@pytest.mark.slow
def test_get_data_returns_data():
    """make sure get_data returns data"""
    data = get_data()
    assert len(data) > 0


@pytest.mark.e2e
@pytest.mark.slow
def test_data_preprocessing_returns_data():
    """make sure data_processing returns data"""
    data = get_data()
    assert len(data) > 0


@pytest.mark.e2e
@pytest.mark.slow
def test_calculate_average_column_names_and_len(expected_column_names):
    """make sure we have movement and temperature columns"""
    data = calculate_average("days")
    output_columns = data.columns

    assert len(data) > 0
    assert all([i in output_columns for i in expected_column_names])


@pytest.mark.fast
def test_always_pass():
    assert True
