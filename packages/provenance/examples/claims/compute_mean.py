"""Compute the mean and count of the mass_kg column. Prints one JSON object
to stdout; the manifest's output_selector picks a field out of it."""
import csv
import json
import sys


def main(path: str) -> None:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    xs = [float(r["mass_kg"]) for r in rows]
    mean = sum(xs) / len(xs)
    print(json.dumps({"mean": mean, "n": len(xs)}))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data.csv")
