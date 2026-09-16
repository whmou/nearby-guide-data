"""Retired bulk geocoder: never overwrite audited points with a first search hit.

Use the per-point evidence workflow in LOCATION_REVIEW.md. This executable stays
as a failing guard for old scripts; prior implementation remains in git history.
"""
import argparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.parse_args()
    parser.error("Retired: automatic coordinate replacement is unsafe; use LOCATION_REVIEW.md")


if __name__ == "__main__":
    main()
