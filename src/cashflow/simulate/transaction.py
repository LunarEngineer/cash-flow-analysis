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
from datetime import date, datetime, timedelta
from numpy.random import default_rng
from src.cashflow import types as cftypes
from typing import Iterable, Mapping, Optional

__all__ = ["Transaction", "_get_random_name"]


class Transaction:
    """Do nothing."""

    def __init__(
        self,
        simulation_length: int,
        simulation_width: int,
        simulation_discretization: str,
        simulation_start_time: cftypes.time = None,
        transaction_time: cftypes.time = None,
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
        # Set the start time
        self.t_0 = _get_timestamp(simulation_start_time)
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
        #
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


def _get_timestamp(datetime_object: cftypes.time):
    """Return formatted data for a timestamp.

    This can take anything interpretable as a datetime object and
    return a named tuple usable by the simulation.

    If elements required aren't present (such as time for a date
    object) they are filled with -1.

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
    TimeStamp(year=2020, month=11, day=23, hour=-1, minute=-1, second=-1)
    >>> _get_timestamp(
    ...     datetime(year=2020,month=11,day=23,hour=2,minute=2,second=2)
    ... )
    TimeStamp(year=2020, month=11, day=23, hour=2, minute=2, second=2)
    >>> _get_timestamp({'year': 2020})
    TimeStamp(year=2020, month=-1, day=-1, hour=-1, minute=-1, second=-1)
    """
    # If it's a datetime we're going to unpack *all* the bits.
    if isinstance(datetime_object, datetime):
        year = datetime_object.year
        month = datetime_object.month
        day = datetime_object.day
        hour = datetime_object.hour
        minute = datetime_object.minute
        second = datetime_object.second
    # If it's a *date* we can't unpack the time; it's meaningless.
    # We are going to fill that with -1.
    elif isinstance(datetime_object, date):
        year = datetime_object.year
        month = datetime_object.month
        day = datetime_object.day
        hour = -1
        minute = -1
        second = -1
    # If it's a *mapping* we assume that all the important bits are
    #   there. If they're not, we are going to shrug and use -1.
    elif isinstance(datetime_object, Mapping):
        year = -1
        month = -1
        day = -1
        hour = -1
        minute = -1
        second = -1
        if "year" in datetime_object:
            year = datetime_object["year"]
        if "month" in datetime_object:
            month = datetime_object["month"]
        if "day" in datetime_object:
            day = datetime_object["day"]
        if "hour" in datetime_object:
            hour = datetime_object["hour"]
        if "minute" in datetime_object:
            minute = datetime_object["minute"]
        if "second" in datetime_object:
            second = datetime_object["second"]
    else:
        raise Exception
    return cftypes.TimeStamp(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )


def _get_indices(transaction: Transaction) -> np.ndarray:
    """Return expected transaction indices.

    This function produces a two dimensional Numpy array of expected
    indices in which a transaction will occur.
    If this is:

    * d_i: A one time event the only requires the start time.
    * d_p: A discrete and periodic event which requires a start time and period.
    * d_a: This is a discrete and aperiodic event. We need to figure that out.
    * p_i: This is probabilistic and instantaneous. We knly need to know the start time and the random function.
    * p_p: This is probabilistic and periodic: We need to know the start time, the period, and the random function.
    * p_a: This is probabilistic and aperiodic: We need to figure that out.

    Returns
    -------
    transaction_indices: np.ndarray
    """
    # What's the sim start time?
    if transaction._transaction_type == "d_i":
        raise NotImplementedError
    elif transaction._transaction_type == "d_p":
        raise NotImplementedError
    elif transaction._transaction_type == "d_a":
        raise NotImplementedError
    elif transaction._transaction_type == "p_i":
        raise NotImplementedError
    elif transaction._transaction_type == "p_p":
        raise NotImplementedError
    elif transaction._transaction_type == "p_a":
        raise NotImplementedError
    return None
