"""The Transaction class is the base class used to define transactions.

A transaction can either be a debit, or a credit.

This class does two things:
1. When started this class does all the heavy lifting to set up the data structure for a transaction object capable of simulating an arbitrary number of transactions.
2. When called with an input vector, an identically shaped output vector, and a 'timestamp' object this class is capable of taking in time formatted input (i.e. day=18)
"""
from typing import Optional
from numpy.random import default_rng

__DISTRIBUTIONS__ = {
    'beta',
    'binomial',
    'chisquare',
    'dirichlet',
	'exponential',
    'f',
	'gamma',
    'geometric',
    'gumbel',
    'hypergeometric',
    'laplace',
    'logistic',
    'lognormal',
    'logseries',
    'multinomial',
    'multivariate_hypergeometric',
    'multivariate_normal',
    'negative_binomial',
    'noncentral_chisquare',
    'noncentral_f',
    'normal',
    'pareto',
    'poisson',
    'power',
    'rayleigh',
    'standard_cauchy',
    'standard_exponential',
    'standard_gamma',
    'standard_normal',
    'standard_t',
    'triangular',
    'uniform',
    'vonmises',
    'wald',
    'weibull',
    'zipf'
}

class Transaction():
    """Do nothing."""
    def __init__(self, number_of_simulated_events: int = 1, seed: Optional[int] = None):
        """Build a transaction model."""
        self._n = number_of_simulated_events
        self._seed = seed
        self._rng = default_rng(seed)
        # Here we need to pick from the numpy random functions appropriately based on input.
        # integers(low[, high, size, dtype, endpoint])
        # random([size, dtype, out])
        # choice(a[, size, replace, p, axis, shuffle])
        # bytes(length)