"""Tests for the Transaction class."""
import pytest
from transactionalsimulator import Transaction, Simulator


test_cases = [
    (
        {
            'simulation_length': 5,
            'number_of_simulations': 5
        },
        1
    )
]


@pytest.mark.parametrize(('simulator_kwargs', 'seed'), test_cases)
def test_transation_init(simulator_kwargs, seed):
    """Test the Transaction class init function."""
    t = Transaction(
        simulator=Simulator(**simulator_kwargs),
        seed=seed
    )

    # Validate properties set appropriately.
    assert t._i == 0
    assert t._n == simulator_kwargs['simulation_length']
    assert t._m == simulator_kwargs['number_of_simulations']
    assert seed == t._seed
