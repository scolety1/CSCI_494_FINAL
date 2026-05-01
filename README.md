# CSCI 494 Final Project

## Thousand Sunny Fleet: Parallel Scheduling for AI Coding Agents

This is my final project for High Performance Computing.

The idea is pretty simple: I built a small simulation of my local coding framework, where multiple software projects are treated like "ships" and each ship can run as an independent worker.

The project compares:

- running three coding jobs one after another
- running the same three coding jobs in parallel

Then it calculates HPC-style metrics:

- speedup
- efficiency
- load imbalance
- total runtime

## Course Concepts Used

### 1. Parallel Programming

Each ship is an independent job. In the parallel version, the ships run at the same time using Python workers.

### 2. HPC Scaling

The script compares sequential time vs parallel wall-clock time.

```text
Speedup = Sequential Time / Parallel Time
Efficiency = Speedup / Number of Workers
```

### 3. Load Imbalance

The three jobs are not the same size. The simple website finishes first, the interactive app takes longer, and the analytical model takes the longest. That means the slowest worker controls the total parallel runtime.

## Files

```text
src/thousand_sunny_fleet.py   Main project code
run_project.ps1               Easy Windows runner
PROJECT_REPORT.md             Short writeup for Canvas
outputs/results.csv           Generated timing data
outputs/run_summary.md        Generated summary
outputs/runtime_chart.png     Generated runtime chart
outputs/worker_timeline.png   Generated worker timeline
```

## How To Run

From this folder:

```powershell
.\run_project.ps1
```

Or with Python:

```powershell
python src/thousand_sunny_fleet.py
```

The script will regenerate the files in `outputs/`.

## What To Submit

For Canvas, I would submit or link this GitHub repo and point to:

- `PROJECT_REPORT.md`
- `src/thousand_sunny_fleet.py`
- `outputs/run_summary.md`
- `outputs/results.csv`
- `outputs/runtime_chart.png`
- `outputs/worker_timeline.png`

