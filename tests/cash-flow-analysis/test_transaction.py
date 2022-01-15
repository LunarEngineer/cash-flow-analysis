"""Tests for the Transaction class."""
import pytest
from cashflowanalysis import Transaction


test_cases = [
    ({'number_of_simulated_events': 1, 'seed': None})
]



def test_transation_init(init_kwargs):
    """Test the Transaction class init function."""
    Transaction(**init_kwargs)