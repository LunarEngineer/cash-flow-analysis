import numpy as np
from numpy.lib.stride_tricks import as_strided


def is_broadcastable(target_array: np.ndarray, broadcast_array: np.ndarray) -> bool:
    """Test if an array is broadcastable to another.

    https://stackoverflow.com/questions/24743753/test-if-an-array-is-broadcastable-to-a-shape/24765997#24765997

    Parameters
    ----------
    target_array: np.ndarray
        The array to broadcast *to*.
    broadcast_array: np.ndarray
        The arrow to attempt to broadcast to the target_array.

    Returns
    -------
    is_broadcastable: bool
        Whether or not the arrays can be broadcast to each other.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1])
    >>> b = np.array([[1, 1], [2, 2]])
    >>> is_broadcastable(a, b)
    True
    >>> is_broadcastable(np.ones((1000, 1000, 1000)), np.ones((1000, 1, 1000)))
    True
    >>> is_broadcastable(np.ones((1000, 1000, 1000)), np.ones((3,)))
    False
    """
    x = np.array([1])
    a = as_strided(x=x, shape=target_array.shape, strides=[0] * len(target_array.shape))
    b = as_strided(
        x=x, shape=broadcast_array.shape, strides=[0] * len(broadcast_array.shape)
    )
    try:
        _ = np.broadcast_arrays(a, b)
        return True
    except ValueError:
        return False
