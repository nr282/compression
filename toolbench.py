"""
The toolbench module will handle the benchmarking of the spectral_compression algorithms.

As was stated previously, the key metrics to measure are:
    1. Speed
    2. Accuracy
    3. Compression Size

Developing a metric class may be useful.

The key goal is to inject the dependencies into the toolbench.


"""
from cloudwatch_logs import CloudwatchLogProtocol, CloudWatchLogsSimulated
from metric import Metric, MetricLogger
from compression import Compression, SpectralCompression, GzipCompression, NoCompression
from typing import List
import os

actual_suffix = '_actual'
decompressed_suffix = '_decompressed'

def toolbench(metric_logger: MetricLogger,
              cloudwatch_logs: CloudwatchLogProtocol,
              compression_algo: List[Compression]
              ):
    """
    Toolbench class tests the spectral_compression and decompression algorithms on cloudwatch logs
    and keeps tracks of metrics.

    """
    print("Develop Cloud Watch Logs...")
    cloudwatch_logs_simulated = cloudwatch_logs.get_data()
    for algo in compression_algo:
        algo_name = algo.get_algo_name()
        file_path = algo.compress(cloudwatch_logs_simulated)
        decompressed_cloudwatch_logs = algo.decompress(file_path)
        comparison = cloudwatch_logs_simulated.merge(decompressed_cloudwatch_logs,
                                                    how='outer',
                                                    validate="one_to_one",
                                                    on="Date",
                                                    suffixes=(actual_suffix, decompressed_suffix))

        comparison["error"] = comparison["Value" + actual_suffix] - comparison["Value" + decompressed_suffix]
        comparison["pct_error_abs"] = comparison["error"].abs() / comparison["Value" + actual_suffix]
        file_size = os.path.getsize(file_path)

        print("-----------------------------------------------")
        print("Compression Algorithm: " + algo_name)
        print("Compression Size: " + str(file_size))
        print("Max Error: " + str(comparison["pct_error_abs"].mean()))
        print("-----------------------------------------------")

if __name__ == '__main__':



    metric_logger = MetricLogger()
    cloudwatch_logs = CloudWatchLogsSimulated()
    gzip_compression = GzipCompression()
    no_compression = NoCompression()
    spectral_compression_algo = SpectralCompression(gzip_compression)

    toolbench(metric_logger,
              cloudwatch_logs,
              [gzip_compression, no_compression, spectral_compression_algo])



