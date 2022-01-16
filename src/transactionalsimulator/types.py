"""Holds commonly used complex types."""
from datetime import datetime
from typing import Mapping, Optional, Union

time = Optional[Union[datetime, Mapping[str, Union[str, int, float]]]]
