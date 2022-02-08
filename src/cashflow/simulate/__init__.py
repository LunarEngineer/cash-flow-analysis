"""Contains the Transaction and Simulation Classes.

A Transaction class is intended to take simple input and construct
the meta-information required to identify when, where, and how it
should fire and what information it requires.

A Simulation class is intended to take multiple Transactions,
queue them appropriately, and fire them all in order.
"""

__all__ = ["index", "error", "nprand", "simulator", "transaction", "array_utilities"]
