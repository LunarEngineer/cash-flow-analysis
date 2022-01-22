"""This exposes Numpy's random distributions in an easy to access format.

This module builds and exposes a data structure allowing for by-name
lookup of Numpy random distributions and their Callable functions
along with their parameters.

Data Structures
---------------
random_names: Set[str]
    This is just a set of the known distributions.
random_callables: Dict[str, Callable]
    This is a by `known distribution` mapping of callable functions.
random_kwargs: Dict[str, Any]
    These are the default keyword arguments.
"""
from typing import Callable

random_names = {
    "beta",
    "binomial",
    "chisquare",
    "dirichlet",
    "exponential",
    "f",
    "gamma",
    "geometric",
    "gumbel",
    "hypergeometric",
    "laplace",
    "logistic",
    "lognormal",
    "logseries",
    "multinomial",
    "multivariate_hypergeometric",
    "multivariate_normal",
    "negative_binomial",
    "noncentral_chisquare",
    "noncentral_f",
    "normal",
    "pareto",
    "poisson",
    "power",
    "rayleigh",
    "standard_cauchy",
    "standard_exponential",
    "standard_gamma",
    "standard_normal",
    "standard_t",
    "triangular",
    "uniform",
    "vonmises",
    "wald",
    "weibull",
    "zipf",
}


# def make_callable(distribution: str, Optional) -> Callable:
#     """Return a Callable handle for a distribution.

#     Parameters
#     ----------
#     distribution: str
#         This is a distribution exposed via random number
#     """

# random_callables = {
#     _: make_callable(_) for _ in random_names
# }


# def _scrape_scipy_dists() -> Sequence[Mapping[str, object]]:
#     """Returns parameter sets for SciPy distributions.

#     Returns
#     -------
#     dist_data: Sequence[Mapping[str, object]]
#         A set of distributions available.

#     Examples
#     --------
#     >>> _scrape_scipy_dists()
#     [{'name': 'thing', 'params': 'thing', 'defaults': 'values', 'docs': 'longstring'}]
#     """
#     dist_info = []
#     _rng = default_rng(0)
#     for distribution in __DISTRIBUTIONS__:
#         fn = getattr(_rng, distribution)
#         inspect.getmembers(
#         dist_info += [
#             {
#                 'name': distribution,
#                 'params': 1,
#                 'defaults': 1,
#                 'docs': fn.__doc__
#             }
#         ]
#     # I'm inspecting the Numpy default_rng implementation.
#     # I've found the Generator items.
#     # from numpy.random import Generator
#     # The Generator is a class. It takes a 'capsule'?
#     # How do I use inspect to inspect it?
#     # No signature
