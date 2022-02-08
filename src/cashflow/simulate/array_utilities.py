"""Holds Numpy or PyArrow array utilities."""

import numpy as np
from numpy.lib.stride_tricks import as_strided


def is_broadcastable(
    target_array_shape: np.ndarray, broadcast_array_shape: np.ndarray
) -> bool:
    """Test if an array is broadcastable to another.

    This function just tests the shape of an array against the shape
    of another array to determine if it *is* broadcastable.

    https://stackoverflow.com/questions/24743753/test-if-an-array-is-broadcastable-to-a-shape/24765997#24765997

    Parameters
    ----------
    target_array_shape: Tuple[int]
        The shape of the array to broadcast *to*.
    broadcast_array_shape: Tuple[int]
        The shape of the array to attempt to broadcast to the target_array.

    Returns
    -------
    is_broadcastable: bool
        Whether or not the arrays can be broadcast to each other.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1])
    >>> b = np.array([[1, 1], [2, 2]])
    >>> is_broadcastable(a.shape, b.shape)
    True
    >>> is_broadcastable((1000, 1000, 1000), (1000, 1, 1000))
    True
    >>> is_broadcastable((1000, 1000, 1000), (3,))
    False
    """
    x = np.array([1])
    a = as_strided(x=x, shape=target_array_shape, strides=[0] * len(target_array_shape))
    b = as_strided(
        x=x, shape=broadcast_array_shape, strides=[0] * len(broadcast_array_shape)
    )
    try:
        _ = np.broadcast_arrays(a, b)
        return True
    except ValueError:
        return False
