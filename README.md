# Parallel Scheduling Experiment

Python coursework for CSCI 494 (High Performance Computing). The experiment measures wall-clock time for three simulated jobs run sequentially and with `ThreadPoolExecutor`.

## What the code demonstrates

- Run independent tasks concurrently and collect their results as workers finish.
- Measure total runtime with `time.perf_counter()` and write per-task timings to CSV.
- Compare speedup and worker efficiency and identify the longest job on the critical path.

The jobs use timed waits with lightweight computation. The result measures overlap for this simulated workload.

## Run it

Use Python 3.9 or later from the repository root.

```sh
python src/thousand_sunny_fleet.py
```

The script regenerates `outputs/results.csv` and `outputs/run_summary.md`. Install Pillow with `python -m pip install pillow` if you also want the generated charts.

## Example run

| Mode | Wall-clock time |
| --- | ---: |
| Sequential | 7.36 s |
| Three workers | 3.50 s |

The recorded run was **2.10× faster** with **70.0% efficiency** across three workers. The longest job determined when the concurrent run could finish.

[Python implementation](src/thousand_sunny_fleet.py) · [Full report](PROJECT_REPORT.md) · [Recorded results](outputs/results.csv) · [Worker timeline](outputs/worker_timeline.png)
