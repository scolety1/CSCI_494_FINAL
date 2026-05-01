# Project Report: Thousand Sunny Fleet

## Project Idea

For my final project, I made a small simulation of an autonomous coding fleet. The framework treats each project like a "ship." Each ship has a job to do, such as building a simple website, building an interactive app, or building an analytical model.

The main question I tested was:

> Can independent coding jobs finish faster when they run in parallel instead of one after another?

## Why This Fits HPC

This project uses at least two major class topics:

1. **Parallel Programming**
   - Multiple independent jobs run at the same time.
   - Each job acts like a separate worker.

2. **HPC Scaling**
   - I compare sequential runtime against parallel wall-clock runtime.
   - I calculate speedup and efficiency.

I also looked at **load imbalance**, because the three jobs are different sizes.

## Workloads

I used three fake coding projects with different difficulty levels:

| Worker | Project | Complexity |
|---|---|---|
| Worker 1 | Saffron Landing | Simple static website |
| Worker 2 | Service Brief | Interactive restaurant manager app |
| Worker 3 | Keeper Lab | Analytical scoring/modeling tool |

The point was not to make the fake jobs perfect. The point was to model the way a fleet of AI coding agents would have uneven workloads.

## Metrics

The script calculates:

```text
Speedup = Sequential Time / Parallel Time
Efficiency = Speedup / Number of Workers
Load Imbalance = (Slowest Worker Time - Average Worker Time) / Average Worker Time
```

## What Worked

The parallel run finished faster than the sequential run. That makes sense because the ships are mostly independent.

The project also showed why scaling is not perfect. Even if three workers run at the same time, the longest job still controls when the whole run is done.

## Challenges

The hardest part was explaining the difference between "running three jobs at once" and "perfect scaling." Parallelism helps, but overhead and uneven job sizes still matter.

This was also a good reminder that a scheduling system needs more than just workers. It also needs:

- task definitions
- health checks
- logs
- output reports
- failure handling

## What I Learned

The biggest thing I learned is that AI coding work can be thought of like a parallel computing workload. If the jobs are independent, parallel execution can improve throughput. But the system still has normal HPC problems: overhead, bottlenecks, and load imbalance.

This made the class topics feel more real to me because I could connect them to a project I actually care about.

## Generated Evidence

The generated evidence is in the `outputs/` folder:

- `results.csv`
- `run_summary.md`
- `runtime_chart.png`
- `worker_timeline.png`

