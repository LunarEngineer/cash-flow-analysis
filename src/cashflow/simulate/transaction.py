"""The Transaction class is the base class used to define transactions.

A transaction can either be a debit, or a credit.

This class does two things:
1. When started this class does all the heavy lifting to set up the data
   structure for a transaction object capable of simulating an arbitrary
   number of transactions dependent on timestep input.
2. When called with an input vector, an identically shaped output vector, and
   a 'timestamp' object this class is capable of taking in time formatted
   input (i.e. day=18), deciding if it needs to trigger, and appropriately
   running internal mechanisms.
"""
import hashlib
import inspect
import numpy as np
from datetime import date, datetime, timedelta
from cashflow.simulate import types as stypes
from typing import Iterable, Mapping, Optional
from numpy.random import default_rng

__DISTRIBUTIONS__ = {
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


class Transaction:
    """Do nothing."""

    def __init__(
        self,
        simulation_length: int,
        simulation_width: int,
        seed: Optional[int] = None,
        start_time: stypes.time = None,
        frequency: Optional[stypes.frequency] = None,
        name: Optional[str] = None,
        **kwargs
    ):
        """Build a transaction model."""
        # The field of transactions we're going to consider is n x m
        # There are n timesteps.
        self._n = simulation_length
        # There are m parallel simulations.
        self._m = simulation_width
        # Set the start time
        self.t_0 = start_time
        # This has prescribed randomness (or not)
        self._seed = seed
        self._rng = default_rng(seed)
        # This has a frequency
        self._f = frequency
        # which can be used to quickly place this transaction into a bucket.
        self._transaction_type: str = _get_transaction_type(frequency)
        # This needs to scrape input still to build probabilistic draw?
        # Finally, this transaction has a name. It *could* be a custom name.
        if name is None:
            name = _get_random_name(self._rng.integers(low=0))
        self._name=name


def _get_transaction_type(frequency: stypes.frequency) -> str:
    """Return type of transaction.

    For a full list of transaction types please view:
    `cashflow.simulate.types`

    This essentially boils down to {discrete | probabilistic} and
    {periodic | aperiodic}.

    Parameters
    ----------
    frequency: stypes.frequency
        The frequency of the transaction.

    Returns
    -------
    transaction_type: str
        The type of the transaction.

    Examples
    --------
    This takes a variety of objects and interprets them.
    Ints are directly translated as a *period* and thus are discrete and periodic.
    >>> _get_transaction_type(2)
    'd_p'

    Floats are directly translated as a *probability* and are thus probabilistic and periodic.
    >>> _get_transaction_type(2.)
    'p_p'

    No frequency? No problem! It's discrete and only happens once.
    >>> _get_transaction_type(None)
    'd_i'

    What if you pass an object interpretable as a datetime?
    It's discrete and *aperiodic*.
    >>> from datetime import datetime
    >>> _get_transaction_type(datetime.now())
    'd_a'

    Ok, what about an object interpretable as a timedelta?
    It's discrete and *periodic*.
    >>> from datetime import timedelta
    >>> _get_transaction_type(timedelta(hours=2))
    'd_p'

    What about lists or arrays of ints?
    >>> import numpy as np
    >>> _get_transaction_type([1, 1, 1])
    'd_a'
    >>> _get_transaction_type(np.array([1, 1, 1]))
    'd_a'
    >>> _get_transaction_type([1., 1., 1.])
    'p_a'
    >>> _get_transaction_type(np.array([1., 1., 1.]))
    'p_a'
    """
    # How do we determine transaction types?
    if frequency is None:
        # I'm only going to happen once!
        return "d_i"
    elif isinstance(frequency, datetime):
        # I'll happen once more
        return "d_a"
    elif isinstance(frequency, (int, timedelta)):
        # I'll happen periodically and reliably.
        return "d_p"
    elif isinstance(frequency, float):
        # A float occurs probabilistically periodically.
        return "p_p"
    elif isinstance(frequency, np.ndarray):
        if np.issubdtype(frequency.dtype, np.floating):
            # Floats are probabilistic, an array is aperiodic.
            return "p_a"
        elif np.issubdtype(frequency.dtype, np.integer):
            # Ints are discrete, an array is aperiodic.
            return "d_a"
    elif isinstance(frequency, Iterable):
        if all(map(lambda x: isinstance(x, (int, timedelta)), frequency)):
            # These are going to happen aperiodically.
            return "d_a"
        elif all(map(lambda x: isinstance(x, float), frequency)):
            return "p_a"
    else:
        raise TypeError


def _get_random_name(seed: int) -> str:
    """Generate a pseudo random name.

    This makes a quasi-pRNG 'name'.
    
    Parameters
    ----------
    seed: int
        This is a seed to hash to create a name.
    
    Returns
    -------
    pseudo_random_hash: str

    Examples
    --------
    >>> _get_random_name(0)
    'cfcd208495d565ef66e7dff9f98764da'
    >>> _get_random_name(1)
    'c4ca4238a0b923820dcc509a6f75849b'
    >>> _get_random_name(2)
    'c81e728d9d4c2f636f067f89cc14862c'
    """
    return hashlib.md5(str(seed).encode('utf-8')).hexdigest()


def _get_timestamp(datetime_object: stypes.time):
    """Return formatted data for a timestamp.
    
    Parameters
    ----------
    datetimeobj: stypes.time
        A timestamp to standardize.

    Returns
    -------
    datetime_object: stypes.TimeStamp
        A TimeStamp

    Examples
    --------
    >>> from datetime import date, datetime
    >>> _get_timestamp(date(year=2020,month=11,day=23))
    TimeStamp(year=2020, month=11, day=23, hour=nan, minute=nan, second=nan)
    >>> _get_timestamp(datetime(year=2020,month=11,day=23,hour=2,minute=2,second=2))
    TimeStamp(year=2020, month=11, day=23, hour=2, minute=2, second=2)
    >>> _get_timestamp({'year': 2020})
    TimeStamp(year=2020, month=nan, day=nan, hour=nan, minute=nan, second=nan)
    """
    if isinstance(datetime_object, datetime):
        year=datetime_object.year
        month=datetime_object.month
        day=datetime_object.day
        hour=datetime_object.hour
        minute=datetime_object.minute
        second=datetime_object.secon
    elif isinstance(datetime_object, date):
        year=datetime_object.year
        month=datetime_object.month
        day=datetime_object.day
        hour=np.nan
        minute=np.nan
        second=np.nan
    elif isinstance(datetime_object, Mapping):
        _datetimecp = datetime_object.copy()
        year=_datetimecp.pop('year', np.nan)
        month=_datetimecp.pop('month', np.nan)
        day=_datetimecp.pop('day', np.nan)
        hour=_datetimecp.pop('hour', np.nan)
        minute=_datetimecp.pop('minute', np.nan)
        second=_datetimecp.pop('second', np.nan)
    else:
        raise Exception
    return stypes.TimeStamp(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second
    )