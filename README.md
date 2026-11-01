# Divide-and-Conquer Algorithms: Quick Sort vs. Merge Sort

## Overview
This project implements Quick Sort and Merge Sort in Python and compares their performance on sorted, reverse-sorted, and randomly generated integer datasets.

## Files
- `Assignment2.py` — algorithm implementations, benchmarking, and graph generation.
- `results.csv` — measured execution-time and peak traced-memory results.
- `sorted_graph.png` — execution-time comparison on sorted input.
- `reverse_sorted_graph.png` — execution-time comparison on reverse-sorted input.
- `random_graph.png` — execution-time comparison on random input.

## Requirements
- Python 3
- Matplotlib for generating graphs

Install Matplotlib if needed:

```bash
python3 -m pip install matplotlib
```

## How to Run
Run the benchmark program:

```bash
python3 Assignment2.py
```

This checks sorting correctness, measures execution time and peak traced memory, writes `results.csv`, and generates the three graphs when Matplotlib is installed.

## Experimental Method
Both algorithms are tested on sorted, reverse-sorted, and random integer lists at several input sizes. Execution time is reported as the median of three runs. Peak traced memory is measured separately with Python's `tracemalloc` module.

Quick Sort uses the last element as the pivot. This intentionally demonstrates how pivot choice can cause poor performance on already sorted or reverse-sorted inputs. Merge Sort divides the input into approximately equal halves and merges the sorted results.

## Theoretical Complexity

| Algorithm | Best case | Average case | Worst case | Auxiliary space |
|---|---|---|---|---|
| Quick Sort | Θ(n log n) | Θ(n log n) | Θ(n²) | Typically O(log n) stack when balanced; O(n) worst-case stack |
| Merge Sort | Θ(n log n) | Θ(n log n) | Θ(n log n) | O(n) |

The space used by the Python implementations also depends on list copies, temporary sublists, and runtime allocation behavior.

## Results
Use the generated `results.csv` and PNG graphs to discuss the measured outcomes. Do not report expected or illustrative values as experimental measurements.

## Author
- Name: [Your Name]
- Course: [Your Course Title]
- Assignment: 2
