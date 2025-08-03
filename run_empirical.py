from selection_algorithms import empirical_compare
import json
import datetime
import os

if __name__ == '__main__':
    results = empirical_compare(sizes=(1000,5000,10000), trials=1)
    out_str = json.dumps(results, indent=2)

    # Print to stdout
    print(out_str)

    # Prepare output filename with timestamp
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = os.path.dirname(__file__)
    fname = os.path.join(out_dir, f"empirical_results_{ts}.txt")

    # Write to file
    with open(fname, "w") as f:
        f.write(out_str)

    print(f"Results written to {fname}")
