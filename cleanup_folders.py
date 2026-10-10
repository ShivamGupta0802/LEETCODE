
from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parent

# Correct LeetCode problem IDs mapped to folder slugs.
PROBLEMS = {
    1: "two-sum",
    4: "median-of-two-sorted-arrays",
    7: "reverse-integer",
    9: "palindrome-number",
    26: "remove-duplicates-from-sorted-array",
    35: "search-insert-position",
    69: "sqrtx",
    74: "search-a-2d-matrix",
    88: "merge-sorted-array",
    121: "best-time-to-buy-and-sell-stock",
    217: "contains-duplicate",
    231: "power-of-two",
    233: "number-of-digit-one",
    240: "search-a-2d-matrix-ii",
    258: "add-digits",
    278: "first-bad-version",
    507: "perfect-number",
    704: "binary-search",
    724: "find-pivot-index",
    1281: "subtract-the-product-and-sum-of-digits-of-an-integer",
    1342: "number-of-steps-to-reduce-a-number-to-zero",
    1351: "count-negative-numbers-in-a-sorted-matrix",
    2119: "a-number-after-a-double-reversal",
    2520: "count-the-digits-that-divide-a-number",
    2529: "maximum-count-of-positive-integer-and-negative-integer",
    3099: "harshad-number",
    344: "reverse-string",
}

def slug_from_folder(name):
    return re.sub(r"^\d+-", "", name)

def merge_missing(source, target):
    """Copy files that are missing; never overwrite existing files."""
    for item in source.rglob("*"):
        relative = item.relative_to(source)
        destination = target / relative

        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)
            print(f"  Copied: {relative}")

def main():
    print("This will consolidate duplicate problem folders.")
    print("Existing destination files will not be overwritten.")
    if input("Type CLEAN to continue: ").strip() != "CLEAN":
        print("Cancelled.")
        return

    directories = [
        p for p in ROOT.iterdir()
        if p.is_dir() and p.name != ".git"
    ]

    renamed = 0

    for problem_id, slug in PROBLEMS.items():
        target = ROOT / f"{problem_id}-{slug}"

        sources = [
            p for p in directories
            if p.exists() and slug_from_folder(p.name) == slug
        ]

        if not sources:
            continue

        target.mkdir(parents=True, exist_ok=True)

        for source in sources:
            if source.resolve() == target.resolve():
                continue

            print(f"Merging: {source.name} -> {target.name}")
            merge_missing(source, target)
            shutil.rmtree(source)
            renamed += 1

        print(f"Kept: {target.name}")

    print("\nCleanup complete.")
    print(f"Duplicate/incorrect folders removed: {renamed}")
    print("Review the folders before committing.")

if __name__ == "__main__":
    main()
