"""
Selection algorithms and empirical comparison utilities.

Includes:
- randomized_quickselect: expected linear-time selection (Quickselect with random pivot)
- deterministic_select: worst-case linear-time selection using Median of Medians
- helpers to generate inputs and compare performance empirically
"""

import random
import time


def randomized_quickselect(arr, k):
    """
    Return the k-th smallest element (1-based) using randomized Quickselect.
    Expected O(n) time on average; worst-case O(n^2) with very low probability.
    Works by choosing a random pivot and partitioning into <, ==, >,
    then recursing on the appropriate partition.
    """
    if not 1 <= k <= len(arr):
        raise IndexError(f"k={k} is out of bounds for array of length {len(arr)}")

    def select(a, k):
        # Base case: single element
        if len(a) == 1:
            return a[0]
        # Random pivot selection
        pivot = random.choice(a)
        # Partition array relative to pivot
        lows = [x for x in a if x < pivot]
        highs = [x for x in a if x > pivot]
        pivots = [x for x in a if x == pivot]
        # Recurse into the partition that contains the k-th smallest
        if k <= len(lows):
            return select(lows, k)
        elif k <= len(lows) + len(pivots):
            return pivot  # pivot is the k-th smallest
        else:
            return select(highs, k - len(lows) - len(pivots))

    # Operate on a copy to avoid mutating caller's list
    return select(list(arr), k)


def deterministic_select(arr, k):
    """
    Return the k-th smallest element (1-based) using the Median of Medians algorithm.
    Provides worst-case O(n) time by carefully choosing a good pivot.
    """
    if not 1 <= k <= len(arr):
        raise IndexError(f"k={k} is out of bounds for array of length {len(arr)}")

    def _select(a, k):
        n = len(a)
        # For small arrays, fallback to sorting (constant factor is fine)
        if n <= 10:
            return sorted(a)[k - 1]

        # Partition into groups of 5 and compute each group's median
        groups = [a[i:i + 5] for i in range(0, n, 5)]
        medians = [sorted(g)[len(g) // 2] for g in groups]

        # Recursively select the median of medians as pivot
        median_of_medians_index = len(medians) // 2 + (1 if len(medians) % 2 else 0)
        pivot = _select(medians, median_of_medians_index)

        # Partition around pivot
        lows = [x for x in a if x < pivot]
        highs = [x for x in a if x > pivot]
        pivots = [x for x in a if x == pivot]

        # Recurse into the correct partition
        if k <= len(lows):
            return _select(lows, k)
        elif k <= len(lows) + len(pivots):
            return pivot
        else:
            return _select(highs, k - len(lows) - len(pivots))

    return _select(list(arr), k)


def generate_inputs(n, distribution='random'):
    """
    Generate test input arrays of size n with different distributions.

    distribution options:
    - 'random': uniformly random integers in [0, 10*n]
    - 'sorted': increasing sequence 0..n-1
    - 'reverse': decreasing sequence
    """
    if distribution == 'random':
        return [random.randint(0, n * 10) for _ in range(n)]
    elif distribution == 'sorted':
        return list(range(n))
    elif distribution == 'reverse':
        return list(range(n))[::-1]
    else:
        raise ValueError('Unknown distribution')


def empirical_compare(sizes=(1000, 5000, 10000), trials=1):
    """
    Compare running times of randomized and deterministic selection algorithms.

    Parameters:
    - sizes: iterable of input sizes to test
    - trials: number of repeated trials (currently not used to average; each size/distribution is run once)

    Returns:
    A list of dicts containing timing results in milliseconds for each combination.
    """
    results = []
    for n in sizes:
        for distro in ['random', 'sorted', 'reverse']:
            arr = generate_inputs(n, distribution=distro)
            k = n // 2  # choose median position for consistency

            # Time randomized Quickselect
            t1 = time.perf_counter()
            _ = randomized_quickselect(arr, k)
            t2 = time.perf_counter()

            # Time deterministic selection
            _ = deterministic_select(arr, k)
            t3 = time.perf_counter()

            results.append({
                'n': n,
                'distribution': distro,
                'randomized_time_ms': (t2 - t1) * 1000,
                'deterministic_time_ms': (t3 - t2) * 1000
            })
    return results


if __name__ == '__main__':
    # Simple usage examples / sanity checks
    print('Example: median of 11 elements (randomized):', randomized_quickselect(list(range(11)), 6))
    print('Example: median of 11 elements reversed (deterministic):', deterministic_select(list(range(11))[::-1], 6))
