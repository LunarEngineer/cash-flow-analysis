"""Holds tools for extracting indices from transactional data."""
import numpy as np
from cashflow import types as cftypes
from cashflow.simulate import error as cfserror, array_utilities as cfsau
from typing import Optional, Type


def _get_indices_periodic(
    start_index: int,
    simulation_length: int,
    simulation_width: int,
    freq: cftypes.frequency,
    rng: Optional[Type[np.random.default_rng]] = None,
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

    This is a simple example. If it's an integer frequency it represents
    a repeating discrete event. A one dimensional array like this one
    will be broadcast across the width of the simulation.

    >>> _get_indices_periodic(
    ...     start_index=0,
    ...     simulation_length=5,
    ...     simulation_width=5,
    ...     freq=2
    ... )
    array([0, 2, 4])

    This is another simple example. If it's a float frequency it
    represents a *uniform random probability*. It needs an RNG object
    passed into it. This example gives all items a uniform probability
    of 0.3. A 5x5 simulation with a .3 probability will yield ~8 indices.

    >>> from numpy.random import default_rng
    >>> rng = default_rng(3)
    >>> _get_indices_periodic(
    ...     start_index=0,
    ...     simulation_length=5,
    ...     simulation_width=5,
    ...     freq=.3,
    ...     rng=rng
    ... ).T
    array([[0, 0, 0, 1, 1, 3, 3, 4, 4],
           [0, 1, 4, 2, 4, 1, 4, 0, 2]])

    These few examples use broadcasting to take an array of
    probabilities instead of a single probability. In the first case
    the probabilities can be interpreted as a single float to use in
    each independent simulation. The shape is (simulation_width, 1).
    Note here that axis 0 is *simulation length* and axis 1 is *width*.
    >>> import numpy as np
    >>> _get_indices_periodic(
    ...     start_index=0,
    ...     simulation_length=5,
    ...     simulation_width=5,
    ...     freq=np.array([[1, .8, .3, .1, 0]]),
    ...     rng=rng
    ... ).T
    array([[0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4],
           [0, 1, 3, 0, 1, 0, 1, 0, 1, 0, 2]])

    In this second case the probabilities can be interpreted as a
    single float to use *in each time step*. Note that almost all
    events happen in the first and second timestep.
    >>> _get_indices_periodic(
    ...     start_index=0,
    ...     simulation_length=5,
    ...     simulation_width=5,
    ...     freq=np.array([1, .8, .3, .1, 0]).reshape(-1, 1),
    ...     rng=rng
    ... ).T
    array([[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2],
           [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]])

    In this third contrived and silly example the probabilities are
    *unique* to every independent timestep acrosss all simulations.
    We mock that by passing an array the size of the simulation.

    >>> probs = rng.random((2,4))
    >>> probs
    array([[0.36928631, 0.08489477, 0.19352758, 0.21386699],
           [0.85864193, 0.12675498, 0.29675777, 0.49284698]])
    >>> _get_indices_periodic(
    ...     start_index=0,
    ...     simulation_length=2,
    ...     simulation_width=4,
    ...     freq=probs,
    ...     rng=rng
    ... ).T
    array([[0, 1, 1],
           [3, 0, 2]])
    """
    if isinstance(freq, int):
        # This is a dsicrete *period*.
        # This will be broadcast
        sorted_periodic_indices = range(start_index, simulation_length, freq)
    elif isinstance(freq, float):
        # This is a *single* float and represents a probability for
        #   all timesteps.
        if rng is None:
            raise cfserror.InputConfigurationError(
                """
            \n[Probabilistic Transaction Frequency]: No rng object available.
            """
            )
        sorted_periodic_indices = np.argwhere(
            rng.random((simulation_length, simulation_width)) <= freq
        )
    elif isinstance(freq, np.ndarray) and np.issubdtype(freq.dtype, np.floating):
        if not cfsau.is_broadcastable(
            freq.shape, (simulation_length, simulation_width)
        ):
            raise cfserror.InputConfigurationError(
                """
            \n[Probabilistic Transaction Frequency]: Probability not broadcastable.
            """
            )
        sorted_periodic_indices = np.argwhere(
            rng.random((simulation_length, simulation_width)) <= freq
        )
    else:
        raise cfserror.InputConfigurationError("Shitass!")
    return np.array(sorted_periodic_indices)
