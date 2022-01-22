"""Holds commonly used complex types.

## Time

A Time, in the terms of the simulation engine, can be one of a few things:
* datetime.datetime.time: This is

## Frequency

A frequency, in the terms of the simulation engine, can be one of a few things:
* int: Integer objects are used to force an event to occur periodically at a
  base resolution defined by the simulation.
* timedelta: Time deltas are used to force an event to occur periodically with
  a period equal to the timedelta.
* float: A float is defined to be a probability drawn from a uniform (0, 1)
  distribution.
* Iterable[int]: An iterable indicating a period of time in which each
  discrete resolution event occurs a number of times equal to the value of the
  integers.
* Iterable[float]: An iterable indicating a period of time in which each
  probabilistic event occurs with probability equal to the value of the
  integers.
* Iterable[time]: Preset times at which to occur.
* Iterable[timedelta]: The period at which this interaction will reoccur.

## Transaction Types

* d_i (discrete instantaneous): This is a transaction that is only handled
  *once*. It is used and discarded.
* d_p (discrete periodic): This is a transaction that occurs at regularly
  scheduled intervals. It is reused.
* d_a (discrete aperiodic): This is a transaction that occurs at irregularly
  scheduled intervals. It is reused.
* p_p (probabilistic periodic): This is a transaction that occurs
  probabilistically at regularly scheduled intervals. It is reused.
* p_a (probabilistic aperiodic): This is a transaction that occurs
  probabilistically at irregularly scheduled intervals. It is reused.
"""
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Iterable, Mapping, Union


@dataclass
class TimeStamp:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int


time = Union[datetime, date, Mapping[str, int], TimeStamp]
frequency = Union[int, float, Iterable[Union[int, float, time, timedelta]], None]

transaction_types = {
    "d_i",
    "d_p",
    "d_a",
    "p_i",
    "p_p",
    "p_a",
}
