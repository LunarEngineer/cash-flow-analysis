"""Tests for the Transaction class."""

import pytest
from datetime import date
from datetime import datetime, timedelta
from cashflow.simulate import transaction as cst, simulator as css


test_cases = [
    (None, 'd_i'),
    (datetime.now(), 'd_a'),
    (1, 'd_p'),
    (timedelta(hours=1), 'd_p'),
    (1., 'p_p'),
    ([1, timedelta(hours=1)], 'd_a'),
    ([1., 1.], 'p_a')
]


@pytest.mark.parametrize(('frequency', 'expectation'), test_cases)
def test__get_transaction_type(frequency, expectation):
    assert cst._get_transaction_type(frequency) == expectation


test_cases = [
    (0, 'cfcd208495d565ef66e7dff9f98764da'),
    (1, 'c4ca4238a0b923820dcc509a6f75849b'),
    (2, 'c81e728d9d4c2f636f067f89cc14862c')
]


@pytest.mark.parametrize(('seed', 'expectation'), test_cases)
def test__get_random_name(seed: int, expectation: str):
    """Test _get_random_name."""
    assert cst._get_random_name(seed) == expectation


test_cases = [
    (
        {
            "simulation_length": 128,
            "simulation_width": 24,
            "seed": 42,
            "start_time": date(2020, 1, 1),
            "frequency": None,
            "name": None,
        },
        {
            '_n': 128,
            '_m': 24,
            '_seed': 42,
            '_t_0': date(2020, 1, 1),
            '_f': None,
            '_transaction_type': 'd_i',
            'name': 'bob'
        }
    )
]


@pytest.mark.parametrize(('simulator_kwargs', 'seed'), test_cases)
def test_transation_init(simulator_kwargs, seed, expected_values):
    """Test the Transaction class init function."""
    t = cst.Transaction(
        simulator=css.Simulator(**simulator_kwargs),
        seed=seed
    )

    # Validate properties set appropriately.
    assert t._i == 0
    assert t._n == expected_values['_n']
    assert t._m == expected_values['_m']
    assert t._seed == expected_values['_seed']
    assert t.t_0 == expected_values['_t_0']
    assert t._f ==  expected_values['_t_f']
