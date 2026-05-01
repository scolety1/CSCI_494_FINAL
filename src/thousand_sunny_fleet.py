from __future__ import annotations

import csv
import math
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except Exception:  # pragma: no cover - output still works without screenshots
    Image = None
    ImageDraw = None
    ImageFont = None


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


@dataclass(frozen=True)
class ShipJob:
    name: str
    description: str
    difficulty_units: int
    seconds_per_unit: float


@dataclass
class ShipResult:
    name: str
    mode: str
    started_at: float
    finished_at: float
    elapsed_seconds: float
    work_units: int
    output_note: str


JOBS = [
    ShipJob(
        name="Saffron Landing",
        description="simple static restaurant website",
        difficulty_units=4,
        seconds_per_unit=0.35,
    ),
    ShipJob(
        name="Service Brief",
        description="interactive manager shift brief app",
        difficulty_units=7,
        seconds_per_unit=0.35,
    ),
    ShipJob(
        name="Keeper Lab",
        description="analytical keeper/drop scoring model",
        difficulty_units=10,
        seconds_per_unit=0.35,
    ),
]


def do_fake_ship_work(job: ShipJob, mode: str, zero_time: float) -> ShipResult:
    """Simulate one independent coding ship doing work.

    This is intentionally simple. The point is to model independent work with
    different durations so the final report can show parallel speedup and load
    imbalance.
    """

    started = time.perf_counter()

    checksum = 0
    for unit in range(job.difficulty_units):
        time.sleep(job.seconds_per_unit)
        checksum += int(math.sqrt((unit + 1) * 10_000))

    finished = time.perf_counter()
    return ShipResult(
        name=job.name,
        mode=mode,
        started_at=started - zero_time,
        finished_at=finished - zero_time,
        elapsed_seconds=finished - started,
        work_units=job.difficulty_units,
        output_note=f"{job.description}; checksum={checksum}",
    )


def run_sequential() -> tuple[list[ShipResult], float]:
    start = time.perf_counter()
    results = [do_fake_ship_work(job, "sequential", start) for job in JOBS]
    return results, time.perf_counter() - start


def run_parallel() -> tuple[list[ShipResult], float]:
    start = time.perf_counter()
    results: list[ShipResult] = []
    with ThreadPoolExecutor(max_workers=len(JOBS)) as executor:
        futures = [executor.submit(do_fake_ship_work, job, "parallel", start) for job in JOBS]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda result: result.started_at)
    return results, time.perf_counter() - start


def calculate_metrics(sequential_time: float, parallel_time: float, parallel_results: list[ShipResult]) -> dict[str, float]:
    workers = len(parallel_results)
    speedup = sequential_time / parallel_time
    efficiency = speedup / workers
    worker_times = [result.elapsed_seconds for result in parallel_results]
    average_worker_time = sum(worker_times) / workers
    slowest_worker_time = max(worker_times)
    load_imbalance = (slowest_worker_time - average_worker_time) / average_worker_time
    return {
        "workers": workers,
        "sequential_time": sequential_time,
        "parallel_time": parallel_time,
        "speedup": speedup,
        "efficiency": efficiency,
        "average_worker_time": average_worker_time,
        "slowest_worker_time": slowest_worker_time,
        "load_imbalance": load_imbalance,
    }


def write_results_csv(sequential_results: list[ShipResult], parallel_results: list[ShipResult]) -> None:
    path = OUT / "results.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "mode",
                "ship",
                "start_seconds",
                "finish_seconds",
                "elapsed_seconds",
                "work_units",
                "output_note",
            ],
        )
        writer.writeheader()
        for result in sequential_results + parallel_results:
            writer.writerow(
                {
                    "mode": result.mode,
                    "ship": result.name,
                    "start_seconds": f"{result.started_at:.3f}",
                    "finish_seconds": f"{result.finished_at:.3f}",
                    "elapsed_seconds": f"{result.elapsed_seconds:.3f}",
                    "work_units": result.work_units,
                    "output_note": result.output_note,
                }
            )


def write_summary(metrics: dict[str, float], parallel_results: list[ShipResult]) -> None:
    slowest = max(parallel_results, key=lambda result: result.elapsed_seconds)
    summary = f"""# Thousand Sunny Fleet Run Summary

## Result

The parallel version finished faster than the sequential version.

| Metric | Value |
|---|---:|
| Workers | {metrics["workers"]:.0f} |
| Sequential time | {metrics["sequential_time"]:.2f} sec |
| Parallel time | {metrics["parallel_time"]:.2f} sec |
| Speedup | {metrics["speedup"]:.2f}x |
| Efficiency | {metrics["efficiency"] * 100:.1f}% |
| Load imbalance | {metrics["load_imbalance"]:.2f} |
| Slowest worker | {slowest.name} |

## My Interpretation

This shows useful speedup, but not perfect scaling. The main bottleneck is that the three jobs are different sizes. The simple website finishes quickly, but the analytical model keeps running longer, so the whole parallel run is limited by the slowest worker.

That is the main HPC idea I wanted to show: adding workers helps, but overhead and load imbalance still matter.
"""
    (OUT / "run_summary.md").write_text(summary, encoding="utf-8")


def draw_runtime_chart(metrics: dict[str, float]) -> None:
    if Image is None:
        return

    image = Image.new("RGB", (1100, 650), "#f8f5ee")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.text((50, 35), "Thousand Sunny Fleet Runtime Comparison", fill="#172033", font=font)

    max_time = max(metrics["sequential_time"], metrics["parallel_time"])
    chart_left = 240
    chart_top = 130
    chart_width = 760
    bar_height = 80
    gap = 90

    rows = [
        ("Sequential", metrics["sequential_time"], "#8c2f39"),
        ("Parallel", metrics["parallel_time"], "#2f6f73"),
    ]

    for index, (label, value, color) in enumerate(rows):
        y = chart_top + index * (bar_height + gap)
        width = int((value / max_time) * chart_width)
        draw.text((50, y + 25), label, fill="#172033", font=font)
        draw.rectangle((chart_left, y, chart_left + width, y + bar_height), fill=color)
        draw.text((chart_left + width + 15, y + 25), f"{value:.2f} sec", fill="#172033", font=font)

    draw.text((50, 470), f"Speedup: {metrics['speedup']:.2f}x", fill="#172033", font=font)
    draw.text((50, 505), f"Efficiency: {metrics['efficiency'] * 100:.1f}%", fill="#172033", font=font)
    draw.text((50, 540), f"Load imbalance: {metrics['load_imbalance']:.2f}", fill="#172033", font=font)
    draw.text((50, 585), "Takeaway: parallel workers help, but the slowest job still controls the finish time.", fill="#172033", font=font)

    image.save(OUT / "runtime_chart.png")


def draw_worker_timeline(results: list[ShipResult]) -> None:
    if Image is None:
        return

    image = Image.new("RGB", (1100, 700), "#f8f5ee")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.text((50, 35), "Parallel Worker Timeline", fill="#172033", font=font)
    max_finish = max(result.finished_at for result in results)
    chart_left = 250
    chart_top = 130
    chart_width = 760
    bar_height = 70
    gap = 70
    colors = ["#c59b48", "#2f6f73", "#8c2f39"]

    for index, result in enumerate(results):
        y = chart_top + index * (bar_height + gap)
        x1 = chart_left + int((result.started_at / max_finish) * chart_width)
        x2 = chart_left + int((result.finished_at / max_finish) * chart_width)
        draw.text((50, y + 20), result.name, fill="#172033", font=font)
        draw.rectangle((x1, y, x2, y + bar_height), fill=colors[index % len(colors)])
        draw.text((x2 + 12, y + 20), f"{result.elapsed_seconds:.2f} sec", fill="#172033", font=font)

    draw.text((50, 585), "The jobs start together, but they do not finish together.", fill="#172033", font=font)
    draw.text((50, 620), "This is load imbalance: the longest job limits the total parallel runtime.", fill="#172033", font=font)
    image.save(OUT / "worker_timeline.png")


def main() -> None:
    OUT.mkdir(exist_ok=True)

    sequential_results, sequential_time = run_sequential()
    parallel_results, parallel_time = run_parallel()
    metrics = calculate_metrics(sequential_time, parallel_time, parallel_results)

    write_results_csv(sequential_results, parallel_results)
    write_summary(metrics, parallel_results)
    draw_runtime_chart(metrics)
    draw_worker_timeline(parallel_results)

    print("Thousand Sunny Fleet experiment complete.")
    print(f"Sequential time: {metrics['sequential_time']:.2f} sec")
    print(f"Parallel time:   {metrics['parallel_time']:.2f} sec")
    print(f"Speedup:         {metrics['speedup']:.2f}x")
    print(f"Efficiency:      {metrics['efficiency'] * 100:.1f}%")
    print(f"Load imbalance:  {metrics['load_imbalance']:.2f}")
    print(f"Outputs written to: {OUT}")


if __name__ == "__main__":
    main()

