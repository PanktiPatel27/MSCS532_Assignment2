"""
Assignment 2: Divide-and-Conquer Algorithms

Implements Quick Sort and Merge Sort, tests them on sorted,
reverse-sorted, and random datasets, and records execution
time and peak traced memory.

"""

import csv
import random
import statistics
import time
import tracemalloc
from pathlib import Path


# ---------------------------------------------------------
# 1. QUICK SORT
# ---------------------------------------------------------

def quick_sort(arr):
    """Sort a list using Quick Sort and return a new list."""

    result = arr.copy()

    def partition(low, high):
        """Partition around the last element."""
        pivot = result[high]
        i = low - 1

        for j in range(low, high):
            if result[j] <= pivot:
                i += 1
                result[i], result[j] = result[j], result[i]

        result[i + 1], result[high] = (
            result[high],
            result[i + 1],
        )

        return i + 1

    def sort(low, high):
        """Recursively sort the two partitions."""
        if low < high:
            pivot_index = partition(low, high)
            sort(low, pivot_index - 1)
            sort(pivot_index + 1, high)

    sort(0, len(result) - 1)
    return result


# ---------------------------------------------------------
# 2. MERGE SORT
# ---------------------------------------------------------

def merge_sort(arr):
    """Sort a list using Merge Sort and return a new list."""

    if len(arr) <= 1:
        return arr.copy()

    middle = len(arr) // 2

    left = merge_sort(arr[:middle])
    right = merge_sort(arr[middle:])

    # Merge the two sorted halves.
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append any remaining elements.
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


# ---------------------------------------------------------
# 3. MEASURE TIME AND PEAK TRACED MEMORY
# ---------------------------------------------------------

def measure_algorithm(algorithm, data, repetitions=3):
    """
    Return median execution time and median peak traced
    memory across multiple independent runs.
    """

    times = []
    memory_values = []

    expected = sorted(data)

    for _ in range(repetitions):
        # Measure execution time.
        start = time.perf_counter()
        result = algorithm(data)
        elapsed = time.perf_counter() - start

        # Verify correctness.
        if result != expected:
            raise AssertionError(
                f"{algorithm.__name__} returned an incorrect result."
            )

        times.append(elapsed)

        # Measure peak traced memory in a separate run.
        tracemalloc.start()

        memory_result = algorithm(data)

        current_bytes, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        if memory_result != expected:
            raise AssertionError(
                f"{algorithm.__name__} failed the memory-run check."
            )

        memory_values.append(peak_bytes / 1024)

    return (
        statistics.median(times),
        statistics.median(memory_values),
    )


# ---------------------------------------------------------
# 4. GENERATE TEST DATASETS
# ---------------------------------------------------------

def create_datasets(size, seed=42):
    """Create sorted, reverse-sorted, and random integer lists."""

    sorted_data = list(range(size))
    reverse_data = list(range(size, 0, -1))

    rng = random.Random(seed + size)
    random_data = [rng.randint(0, size * 10) for _ in range(size)]

    return {
        "Sorted": sorted_data,
        "Reverse-sorted": reverse_data,
        "Random": random_data,
    }


# ---------------------------------------------------------
# 5. RUN THE EXPERIMENTS
# ---------------------------------------------------------

def main():
    output_dir = Path(__file__).resolve().parent
    csv_path = output_dir / "results.csv"

    # Keep sizes moderate because last-pivot Quick Sort can
    # require quadratic time and deep recursion on ordered data.
    dataset_sizes = [100, 300, 600]

    algorithms = {
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
    }

    results = []

    for size in dataset_sizes:
        datasets = create_datasets(size)

        for dataset_name, data in datasets.items():
            print(
                f"\nDataset: {dataset_name}, "
                f"Size: {size}"
            )

            for algorithm_name, algorithm in algorithms.items():
                elapsed, peak_memory = measure_algorithm(
                    algorithm,
                    data,
                    repetitions=3,
                )

                row = {
                    "Dataset": dataset_name,
                    "Size": size,
                    "Algorithm": algorithm_name,
                    "Median Time (seconds)": elapsed,
                    "Median Peak Traced Memory (KiB)": peak_memory,
                }

                results.append(row)

                print(
                    f"{algorithm_name}: "
                    f"{elapsed:.6f} seconds, "
                    f"{peak_memory:.2f} KiB peak traced memory"
                )

    # Save the measured results to a CSV file.
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "Dataset",
            "Size",
            "Algorithm",
            "Median Time (seconds)",
            "Median Peak Traced Memory (KiB)",
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {csv_path}")

    # Attempt to create a graph if matplotlib is installed.
    try:
        import matplotlib.pyplot as plt

        for dataset_name in ("Sorted", "Reverse-sorted", "Random"):
            plt.figure()

            for algorithm_name in algorithms:
                subset = [
                    row for row in results
                    if row["Dataset"] == dataset_name
                    and row["Algorithm"] == algorithm_name
                ]

                subset.sort(key=lambda row: row["Size"])

                sizes = [row["Size"] for row in subset]
                times = [
                    row["Median Time (seconds)"]
                    for row in subset
                ]

                plt.plot(
                    sizes,
                    times,
                    marker="o",
                    label=algorithm_name,
                )

            plt.xlabel("Input Size (n)")
            plt.ylabel("Median Execution Time (seconds)")
            plt.title(f"Sorting Performance: {dataset_name} Data")
            plt.legend()
            plt.tight_layout()

            graph_path = (
                output_dir
                / f"{dataset_name.lower().replace('-', '_')}_graph.png"
            )

            plt.savefig(graph_path)
            plt.close()

            print(f"Graph saved to: {graph_path}")

    except ImportError:
        print(
            "\nMatplotlib is not installed. "
            "The CSV results were still saved."
        )
        print(
            "To enable graphs, run: "
            "python3 -m pip install matplotlib"
        )


if __name__ == "__main__":
    main()