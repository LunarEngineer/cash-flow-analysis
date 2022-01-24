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
import numpy as np
from datetime import datetime, timedelta
from numpy.random import default_rng
from cashflow import types as cftypes
from cashflow.simulate import error as cfserror
from typing import Iterable, Optional, Type

__all__ = ["Transaction", "_get_random_name"]


class Transaction:
    """Do nothing."""

    def __init__(
        self,
        simulation_length: int,
        simulation_width: int,
        simulation_discretization: str,
        transaction_time: int = 0,
        seed: Optional[int] = None,
        frequency: Optional[cftypes.frequency] = None,
        name: Optional[str] = None,
    ) -> None:
        """Build a transaction object.

        This creates a transaction object.

        Parameters
        ----------
        simulation_length: int
            A number of timesteps to run for.
        simulation_width: int
            How many parallel simulations to account for.
        simulation_discretization: str = 'day'
            The default discretization for the simulation.
            {'second', 'minute', 'hour', 'day', 'month', 'year'}
        simulation_start_time: cftypes.time = None
            This is a timestamp denoting when the simulation starts.
        transaction_time: cftypes.time = None
            This is a timestamp denoting when the transaction fires
            for the first time.
        """
        # The field of transactions we're going to consider is n x m
        # There are n timesteps.
        self._n = simulation_length
        # There are m parallel simulations.
        self._m = simulation_width
        # Set the initial transaction time.
        self.t_0 = transaction_time
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
            # But if it's not we'll just give it a *pretty random* name.
            name = _get_random_name(self._rng.integers(low=0, high=int(1e6)))
        self._name = name
        # Declare where
        self._presence = _get_indices(
            self,
        )


def _get_transaction_type(frequency: cftypes.frequency) -> str:
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
    Ints are directly translated as a *period* and thus are discrete
    and periodic.
    >>> _get_transaction_type(2)
    'd_p'

    Floats are directly translated as a *probability* and are thus
    probabilistic and periodic.
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
        ttype = "d_i"
    elif isinstance(frequency, datetime):
        # I'll happen once more
        ttype = "d_a"
    elif isinstance(frequency, (int, timedelta)):
        # I'll happen periodically and reliably.
        ttype = "d_p"
    elif isinstance(frequency, float):
        # A float occurs probabilistically periodically.
        ttype = "p_p"
    elif isinstance(frequency, np.ndarray):
        if np.issubdtype(frequency.dtype, np.floating):
            # Floats are probabilistic, an array is aperiodic.
            ttype = "p_a"
        elif np.issubdtype(frequency.dtype, np.integer):
            # Ints are discrete, an array is aperiodic.
            ttype = "d_a"
    elif isinstance(frequency, Iterable):
        if all(map(lambda x: isinstance(x, (int, timedelta)), frequency)):
            # These are going to happen aperiodically.
            ttype = "d_a"
        elif all(map(lambda x: isinstance(x, float), frequency)):
            ttype = "p_a"
    else:
        raise TypeError
    return ttype


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
    return hashlib.md5(str(seed).encode("utf-8")).hexdigest()


def _get_indices(transaction: Transaction) -> np.ndarray:
    """Return expected transaction indices.

    This function produces a two dimensional Numpy array of expected
    indices in which a transaction will occur.
    If this is:

    All transactions require the simulation start time.

    * d_i: A one time event only requires the start time of the
        simulation and the start time of the transaction.
    * d_p: A discrete and periodic event which requires a start time
        and period.
    * d_a: This is a discrete and aperiodic event. We need to figure that out.
    * p_i: This is probabilistic and instantaneous. We knly need to know the
     start time and the random function.
    * p_p: This is probabilistic and periodic: We need to know the start time,
     the period, and the random function.
    * p_a: This is probabilistic and aperiodic: We need to figure that out.

    Returns
    -------
    transaction_indices: np.ndarray

    Examples
    --------
    >>> print(1)
    1
    """
    # What's the transactions basic type?
    t_type = transaction._transaction_type
    if t_type == "d_i":
        # If instantaneous and discrete it's pretty easy!
        transaction_indices = transaction.t_0
    elif t_type == "d_p":
        transaction_indices = _get_indices_periodic(
            start_index=transaction.t_0,
            simulation_length=transaction._n,
            freq=transaction._f,
        )
    elif t_type == "d_a":
        raise NotImplementedError
    elif t_type == "p_i":
        raise NotImplementedError
    elif t_type == "p_p":
        transaction_indices = _get_indices_periodic(
            start_index=transaction.t_0,
            simulation_length=transaction._n,
            freq=transaction._f,
        )
    elif t_type == "p_a":
        raise NotImplementedError
    return transaction_indices


def _get_indices_periodic(
    start_index: int,
    simulation_length: int,
    simulation_width: int,
    freq: cftypes.frequency,
    rng: Optional[Type[default_rng]] = None,
) -> np.ndarray:
    """Returns periodic indices.

    Parameters
    ----------

    Returns
    -------
    sorted_periodic_indices
        The sorted set of periodic indices.

    Examples
    --------
    >>> _get_indices_periodic(
    ...     start_index=0,
    ...     simulation_length=5,
    ...     simulation_width=5,
    ...     freq=2
    ... )
    array([0, 2, 4])
    """
    if isinstance(freq, int):
        # This is a *period*.
        # This is discrete.
        # This will be broadcast
        sorted_periodic_indices = range(start_index, simulation_length, freq)
    elif isinstance(freq, float):
        # This is a *single* float and represents a probability for
        #   all timesteps.
        sorted_periodic_indices = np.argwhere(
            rng.random((simulation_length, simulation_width)) > 0
        ).ravel()
    elif isinstance(freq, np.ndarray) and np.issubdtype(freq.dtype, np.floating):
        raise NotImplementedError
    else:
        raise cfserror.InputConfigurationError("Shitass!")
    return np.array(sorted_periodic_indices)


# Create a memory mapped array
# https://arrow.apache.org/docs/python/generated/pyarrow.create_memory_map.html
