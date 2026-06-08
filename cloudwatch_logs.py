"""
Cloudwatch logs are critical for this project, and will form the basis
of our application of spectral_compression to AWS.

Design:
-------
    1. Load from historical data
    2. Simulate the cloud watch log
    3. Encapsulation will be done with an Abstract Cloudwatch Log Class or a Protocol.
        - Now that I think more about it, I think a Protocol will better.
    4. We can then have two classes which will implement the Cloudwatch Log Protocol.


"""

from typing import Protocol
import pandas as pd
import pandera as pa
from pandera.typing import DataFrame, Series
from typing import Protocol
import numpy as np

# Define the pandera schema
class NumericData(pa.DataFrameModel):
    Date: pa.DateTime
    Value: pa.Int

class CloudwatchLogProtocol(Protocol):
    def get_data(self) -> DataFrame[NumericData]:
        pass


class CloudWatchLogsSimulated(object):

    def get_data(self) -> DataFrame[NumericData]:

        time_index = pd.date_range(start="2026-06-01 00:00:00",
                                   end="2026-06-07 00:00:00",
                                   freq="s")

        df = pd.DataFrame()
        df["Date"] = time_index
        df["Value"] = np.random.randint(low=0,
                                        high=10,
                                        size=len(time_index),
                                        dtype=int)

        return df


class CloudWatchLogsHistorical(object):

    def get_data(self) -> DataFrame[NumericData]:
        pass

