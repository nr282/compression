"""
Compression algorithms are critical to modern computer science
and software engineering.

The design of this codebase requires a few things:
    1. Compression Algorithms Implemented as Strategies
    2. Simulation of Cloud Watch Logs
    3. Real Cloud Watch Logs
    3. Comparison of Compression Algorithms


                        Cloud Watch Logs                                - Cloud Watch Logs (Use a class for this)
        <----------------------|------------------------>               |
    Simulated                                       Historical          |
        ---------------------->|<------------------------               |
                               |                                        |
                               |                                        |
                               v                                        |
                            Compress                                    - Compression (Use standard averaging, aggregation)
                                |                                       -
                                |                                       |
                                v                                       |
                    Compressed Cloud Watch Logs                         - Storage
                                |                                       |
                                |                                       |
                                v                                       |
                Decompress with Calculus of Variations                  Decompression (Strategy Pattern)
                                |                                       |
                                |                                       |
                                v                                       |
                    Decompressed Cloud Watch Logs                       Decompressed Dataset


Toolbench
    - Takes in a spectral_compression algorithm (which includes the decompression)
    - Takes in the cloud watch logs with the Protocol
    - Compares the relevant characteristics including:
        - Speed, Compression Size, Accuracy (ie Error)
        -
    -
"""