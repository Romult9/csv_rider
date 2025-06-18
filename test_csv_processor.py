import pytest
import csv
import os
from csv_processor import read_csv, apply_filter, apply_aggregation


@pytest.fixture
def sample_csv(tmp_path):
    data = [
        ['name', 'brand', 'price', 'rating'],
        ['iphone 15 pro', 'apple', '999', '4.9'],
        ['galaxy s23 ultra', 'samsung', '1199', '4.8'],
        ['redmi note 12', 'xiaomi', '199', '4.6'],
        ['poco x5 pro', 'xiaomi', '299', '4.4'],
    ]
    
    file_path = os.path.join(tmp_path, 'test.csv')
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    return file_path


def test_read_csv(sample_csv):
    data = read_csv(sample_csv)
    assert len(data) == 4
    assert data[0]['name'] == 'iphone 15 pro'
    assert data[1]['brand'] == 'samsung'


def test_filter_equal(sample_csv):
    data = read_csv(sample_csv)
    filtered = apply_filter(data, 'brand=xiaomi')
    assert len(filtered) == 2
    assert all(row['brand'] == 'xiaomi' for row in filtered)


def test_filter_greater(sample_csv):
    data = read_csv(sample_csv)
    filtered = apply_filter(data, 'price>500')
    assert len(filtered) == 2
    assert all(float(row['price']) > 500 for row in filtered)


def test_filter_less(sample_csv):
    data = read_csv(sample_csv)
    filtered = apply_filter(data, 'rating<4.7')
    assert len(filtered) == 2
    assert all(float(row['rating']) < 4.7 for row in filtered)


def test_aggregation_avg(sample_csv):
    data = read_csv(sample_csv)
    result = apply_aggregation(data, 'price=avg')
    assert 'avg' in result
    assert result['avg'] == pytest.approx((999 + 1199 + 199 + 299) / 4)


def test_aggregation_min(sample_csv):
    data = read_csv(sample_csv)
    result = apply_aggregation(data, 'rating=min')
    assert 'min' in result
    assert result['min'] == 4.4


def test_aggregation_max(sample_csv):
    data = read_csv(sample_csv)
    result = apply_aggregation(data, 'price=max')
    assert 'max' in result
    assert result['max'] == 1199


def test_non_numeric_aggregation(sample_csv):
    data = read_csv(sample_csv)
    with pytest.raises(ValueError):
        apply_aggregation(data, 'brand=avg')


def test_invalid_filter_format(sample_csv):
    data = read_csv(sample_csv)
    with pytest.raises(ValueError):
        apply_filter(data, 'invalid condition')


def test_invalid_aggregation_format(sample_csv):
    data = read_csv(sample_csv)
    with pytest.raises(ValueError):
        apply_aggregation(data, 'invalid format')