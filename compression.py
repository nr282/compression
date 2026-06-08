"""
Decompression algorithms are required.

Module abstracts the compression algorithms.

Compression Algorithms can include:
    1. Deflate
    2. LZ4
    3. SpecTech




"""


import datetime
from typing import Protocol
import pandas as pd

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
        self.compression_algo = compression_algo

    def compress(self, data: pd.DataFrame) -> str:
        pass

    def decompress(self, path: str):
        pass

    def get_algo_name(self) -> str:
        return "spectral_compression"