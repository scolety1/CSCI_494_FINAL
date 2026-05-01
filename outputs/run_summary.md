# Thousand Sunny Fleet Run Summary

## Result

The parallel version finished faster than the sequential version.

| Metric | Value |
|---|---:|
| Workers | 3 |
| Sequential time | 7.36 sec |
| Parallel time | 3.50 sec |
| Speedup | 2.10x |
| Efficiency | 70.0% |
| Load imbalance | 0.43 |
| Slowest worker | Keeper Lab |

## My Interpretation

This shows useful speedup, but not perfect scaling. The main bottleneck is that the three jobs are different sizes. The simple website finishes quickly, but the analytical model keeps running longer, so the whole parallel run is limited by the slowest worker.

That is the main HPC idea I wanted to show: adding workers helps, but overhead and load imbalance still matter.
