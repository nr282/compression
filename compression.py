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
from spectral_compression.spectral_compression.FDTT import pandas_add_on

class Compression(Protocol):

    def compress(self, data: pd.DataFrame):
        pass

    def decompress(self, data: pd.DataFrame):
        pass

    def get_algo_name(self) -> str:
        pass



class GzipCompression(object):

    def compress(self, data: pd.DataFrame):
        path = "data.csv"
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


    def _apply_spectral_compression(self):
        pass

    def compress(self, data: pd.DataFrame) -> str:
        """
        Compression involves averaging and then applying the standard compression algorithm.

        """

        data.set_index('Date', inplace=True)
        data = data.resample('1min').sum().reset_index()
        path = self.standard_compression_algo.compress(data)
        return path


    def decompress(self, path: str):

        data = pd.read_csv(path, parse_dates=['Date'], dtype={'Date': str})
        result = pandas_add_on.solve_pandas_series(data)


        import pdb
        pdb.set_trace()

    def get_algo_name(self) -> str:
        return "spectral_compression"