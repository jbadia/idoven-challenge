import numpy as np
from modules.metrics import count_zero_crossings_per_lead

def test_count_zero_crossings_per_lead_dask_single_zero_crossing():
    signal = np.array([1, -1, -1, 1, 1, -1, -1, 1])
    expected_result = 4  # The signal has two zero crossings
    result = count_zero_crossings_per_lead(signal)
    assert result == expected_result

def test_count_zero_crossings_per_lead_dask_multiple_zero_crossings():
    signal = np.array([-1, 1, -1, 1, -1, 1, -1, 1])
    expected_result = 7  # The signal has seven zero crossings
    result = count_zero_crossings_per_lead(signal)
    assert result == expected_result

def test_count_zero_crossings_per_lead_dask_no_zero_crossing():
    signal = np.array([1, 1, 1, 1, 1, 1, 1])
    expected_result = 0  # The signal has no zero crossings
    result = count_zero_crossings_per_lead(signal)
    assert result == expected_result

def test_count_zero_crossings_per_lead_dask_all_zero_signal():
    signal = np.array([0, 0, 0, 0, 0])
    expected_result = 0  # The signal has no zero crossings
    result = count_zero_crossings_per_lead(signal)
    assert result == expected_result

def test_count_zero_crossings_per_lead_large_signal():
    signal = signal = (np.arange(0, 100002) % 3) - 1
    expected_result = (signal.size / 3) * 2 - 1
    result = count_zero_crossings_per_lead(signal)
    assert result == expected_result