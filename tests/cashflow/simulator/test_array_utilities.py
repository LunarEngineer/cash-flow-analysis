import pytest
from src.cashflow.simulate import array_utilities as sau


test_cases = [
    ((100, 100, 100), (100, 1, 100)),
    ((100, 100, 100), (100, 1)),
    ((100, 100, 100), (100,)),
    ((100, 100, 100), (1,)),
]


@pytest.mark.parametrize(("shape_1", "shape_2"), test_cases)
def test_is_broadcastable(shape_1, shape_2):
    """Test is_broadcastable."""
    assert sau.is_broadcastable(shape_1, shape_2)
