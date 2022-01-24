# """Tests for the Transaction class."""

# import pytest
# from datetime import date
# from datetime import datetime, timedelta
# from src.cashflow.simulate import transaction as cst
# from src.cashflow.types import TimeStamp

# test_cases = [
#     (None, "d_i"),
#     (datetime.now(), "d_a"),
#     (1, "d_p"),
#     (timedelta(hours=1), "d_p"),
#     (1.0, "p_p"),
#     ([1, timedelta(hours=1)], "d_a"),
#     ([1.0, 1.0], "p_a"),
# ]


# @pytest.mark.parametrize(("frequency", "expectation"), test_cases)
# def test__get_transaction_type(frequency, expectation):
#     assert cst._get_transaction_type(frequency) == expectation


# test_cases = [
#     (0, "cfcd208495d565ef66e7dff9f98764da"),
#     (1, "c4ca4238a0b923820dcc509a6f75849b"),
#     (2, "c81e728d9d4c2f636f067f89cc14862c"),
# ]


# @pytest.mark.parametrize(("seed", "expectation"), test_cases)
# def test__get_random_name(seed: int, expectation: str):
#     """Test _get_random_name."""
#     assert cst._get_random_name(seed) == expectation


# test_cases = [
#     (  # type: ignore
#         {
#             "simulation_length": 128,
#             "simulation_width": 24,
#             "seed": 42,
#             "start_time": date(2020, 1, 1),
#             "frequency": None,
#             "name": None,
#         },
#         {
#             "_n": 128,
#             "_m": 24,
#             "_seed": 42,
#             "_t_0": TimeStamp(2020, 1, 1, -1, -1, -1),
#             "_f": None,
#             "_transaction_type": "d_i",
#             "_name": "51b095073154e7595e022a9b839692ca",
#         },
#     ),  # Discrete and instantaneous
#     (  # type: ignore
#         {
#             "simulation_length": 10,
#             "simulation_width": 5,
#             "seed": 13,
#             "start_time": date(2020, 1, 1),
#             "frequency": 1,
#             "name": None,
#         },
#         {
#             "_n": 10,
#             "_m": 5,
#             "_seed": 13,
#             "_t_0": TimeStamp(2020, 1, 1, -1, -1, -1),
#             "_f": 1,
#             "_transaction_type": "d_p",
#             "_name": "5b987799bd2c2e9ed6686ab1ec064ec1",
#         },
#     ),  # Discrete and periodic
# ]


# @pytest.mark.parametrize(("transaction_kwargs", "expected_values"), test_cases)
# def test_transaction_init(transaction_kwargs, expected_values):
#     """Test the Transaction class init function."""
#     t = cst.Transaction(**transaction_kwargs)

#     ##########################################
#     # Validate properties set appropriately. #
#     ##########################################
#     # n: simulation length
#     assert t._n == expected_values["_n"]
#     # m: simulation width
#     assert t._m == expected_values["_m"]
#     # seed: random seed
#     assert t._seed == expected_values["_seed"]
#     # t_0: first time step in the simulation
#     assert t.t_0 == expected_values["_t_0"]
#     # f: frequency of the simulation
#     assert t._f == expected_values["_f"]
#     # transaction type: Computation bin
#     assert t._transaction_type == expected_values["_transaction_type"]
#     # name: name of the transaction
#     assert t._name == expected_values["_name"]
