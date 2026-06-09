"""
Decompression algorithms are required.

Module abstracts the spectral_compression algorithms.

Compression Algorithms can include:
    1. Deflate
    2. LZ4
    3. Spectral Compression


TODO: Very close to finishing this project

"""

from typing import Protocol

import pandas as pd
from spectral_compression.spectral_compression.FDTT.variational_framework import VariationalFramework, IntegralConstraintElement, IntegralConstraint

class Compression(Protocol):

    def compress(self, data: pd.DataFrame, path=""):
        pass

    def decompress(self, data: pd.DataFrame):
        pass

    def get_algo_name(self) -> str:
        pass



class GzipCompression(object):

    def compress(self, data: pd.DataFrame, path = "data.csv"):
        data.to_csv(path, compression="gzip")
        return path

    def decompress(self, path: str):

        data_types = {
            'Value': int
        }
        df = pd.read_csv(path, compression="gzip",  parse_dates=['Date'], dtype=data_types)
        return df

    def get_algo_name(self) -> str:
        return "gzip_compression"


class NoCompression(object):

    def compress(self, data: pd.DataFrame):
        path = "no_compression.csv"
        data.to_csv(path, index=False)
        return path

    def decompress(self, path: str):
        data_types = {
            'Value': int
        }
        df = pd.read_csv(path, parse_dates=['Date'], dtype=data_types)
        return df

    def get_algo_name(self) -> str:
        return "no_compression"


class SpectralCompression(object):

    def __init__(self, compression_algo: Compression):
        self.standard_compression_algo = compression_algo


    def _apply_spectral_compression(self, data: pd.DataFrame):
        """
        Applies the spectral compression algorithm to the given data.


        """

        start_time = data["Date"].min()
        data["start_time"] = data["Date"].apply(lambda datetime: (datetime - start_time).total_seconds())
        data["end_time"] = data["start_time"].shift(-1)
        data.loc[len(data) - 1, "end_time"] = data.loc[len(data) - 1, "start_time"] + 60
        global_start_time = data.loc[0, "start_time"]
        global_end_time = data.loc[len(data)-1, "end_time"]
        integral_constraints = []
        number_of_functions = 1
        constraint_id = 1
        for index, row in data.iterrows():
            start_time = row["start_time"]
            end_time = row["end_time"]
            value = row["Value"]

            elem = IntegralConstraintElement(1, start_time, end_time, constraint_id)
            constraint = IntegralConstraint([elem], value, constraint_id)
            integral_constraints.append(constraint)
            constraint_id += 1




        # Apply the integral constraints to the Variational Framework.
        framework = VariationalFramework(integral_constraints,
                                         number_of_functions,
                                         global_start_time,
                                         global_end_time)

        # Solve the dataframe.
        framework.solve(check_integral_result=True)

        raise NotImplementedError("Not fully implemented yet...")


    def compress(self, data: pd.DataFrame) -> str:
        """
        Compression involves averaging and then applying the standard compression algorithm.

        """
        path = "spectral_compression.csv"
        data.set_index('Date', inplace=True)
        data = data.resample('1min').sum().reset_index()
        path = self.standard_compression_algo.compress(data, path=path)
        return path


    def decompress(self, path: str):

        data = pd.read_csv(path, parse_dates=['Date'], dtype={'Date': str}, compression="gzip")
        data = data[["Date", "Value"]]
        decompressed_df = self._apply_spectral_compression(data)
        return decompressed_df


    def get_algo_name(self) -> str:
        return "spectral_compression"