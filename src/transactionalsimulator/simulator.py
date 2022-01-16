"""Holds the simulator object."""

import numpy as np
from datetime import datetime
from typing import Iterable, Optional, Mapping


class Simulator():
    """Does nothing, yet."""
    def __init__(
        self,
        simulation_length: int,
        number_of_simulations: int,
        start_time: Optional[datetime],
        transactions: Iterable[Mapping[str, str]]
    ) -> None:
        """Set up simulator class."""
        self._i = 0
        self._n = simulation_length
        self._m = number_of_simulations
        self._history = np.zeros((self._n, self._m))

    def _build_transactions():
        """Build transactions"""
        # Each time has a month, day, year
        # When the transaction is read in the tr
        pass

    def step():
        """Advance world one step"""
        pass
