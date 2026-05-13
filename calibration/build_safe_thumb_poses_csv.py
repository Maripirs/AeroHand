"""
build_safe_thumb_poses_csv.py

Converts the raw human-in-the-loop thumb clearance calibration results into a
usable CSV of safe thumb poses.

Raw input format, produced by calibrate_thumb_clearance.py / testThumb.py:
    thumb_1, thumb_2, thumb_3, finger, start_pose, target_pose, result

Usable output format:
    finger, thumb_1, thumb_2, thumb_3

Only rows marked safe with result == "s" are included. Duplicate rows are removed.
Rows marked unsafe/questionable/skipped are not included.

Usage:
    python3 build_safe_thumb_poses_csv.py

Optional:
    python3 build_safe_thumb_poses_csv.py \
        --input thumb_clearance_results.csv \
        --output safe_thumb_poses_clean.csv

To include the emergency neutral thumb pose [0, 0, 0] for each finger:
    python3 build_safe_thumb_poses_csv.py --include-emergency
"""

import argparse
import csv
from pathlib import Path


DEFAULT_INPUT_FILE = "thumb_clearance_results.csv"
DEFAULT_OUTPUT_FILE = "safe_thumb_poses_clean.csv"

VALID_FINGERS = ["index", "middle", "ring"]
SAFE_RESULT = "s"
EMERGENCY_THUMB_POSE = (0, 0, 0)

# These are poses that were marked safe in the raw calibration file but removed
# from the cleaned usable CSV. Keep this list if you want to reproduce the
# current cleaned dataset exactly. Clear this set if you want every "s" row.
EXCLUDED_SAFE_POSES = {
    ("index", 0, 0, 0),
    ("index", 0, 0, 30),
    ("index", 0, 40, 30),
    ("index", 0, 40, 60),
    ("index", 0, 80, 0),
    ("index", 0, 100, 0),
    ("index", 40, 0, 0),
    ("index", 40, 0, 30),
    ("index", 40, 0, 60),
    ("index", 40, 40, 0),
    ("index", 80, 0, 0),
    ("index", 100, 0, 0),

    ("middle", 0, 0, 0),
    ("middle", 0, 0, 30),
    ("middle", 0, 40, 30),
    ("middle", 0, 40, 60),
    ("middle", 0, 80, 0),
    ("middle", 0, 100, 0),
    ("middle", 40, 0, 0),
    ("middle", 40, 0, 30),
    ("middle", 40, 0, 60),
    ("middle", 40, 40, 0),
    ("middle", 80, 0, 0),
    ("middle", 100, 0, 0),

    ("ring", 0, 0, 0),
    ("ring", 0, 0, 30),
    ("ring", 0, 40, 30),
    ("ring", 0, 40, 60),
    ("ring", 0, 80, 0),
    ("ring", 0, 100, 0),
    ("ring", 40, 0, 0),
    ("ring", 40, 0, 30),
    ("ring", 40, 0, 60),
    ("ring", 40, 40, 0),
    ("ring", 40, 80, 60),
    ("ring", 80, 0, 0),
    ("ring", 80, 40, 30),
    ("ring", 100, 0, 0),
}


def parse_int(row, column_name):
    """Read an integer column with a clear error message."""
    try:
        return int(row[column_name])
    except KeyError as error:
        raise KeyError(f"Missing required column: {column_name}") from error
    except ValueError as error:
        value = row.get(column_name)
        raise ValueError(f"Column {column_name} must be an integer, got {value!r}") from error


def load_safe_thumb_poses(input_path, use_exclusion_list=True):
    """
    Load raw calibration rows and return sorted safe thumb poses.

    Returns a list of tuples:
        (finger, thumb_1, thumb_2, thumb_3)
    """
    safe_poses = set()

    with open(input_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            result = row.get("result", "").strip().lower()
            if result != SAFE_RESULT:
                continue

            finger = row.get("finger", "").strip().lower()
            if finger not in VALID_FINGERS:
                continue

            pose = (
                finger,
                parse_int(row, "thumb_1"),
                parse_int(row, "thumb_2"),
                parse_int(row, "thumb_3"),
            )

            if use_exclusion_list and pose in EXCLUDED_SAFE_POSES:
                continue

            safe_poses.add(pose)

    return sorted(
        safe_poses,
        key=lambda item: (
            VALID_FINGERS.index(item[0]),
            item[1],
            item[2],
            item[3],
        ),
    )


def add_emergency_pose(safe_poses):
    """Add [0, 0, 0] for each finger if it is not already present."""
    pose_set = set(safe_poses)

    for finger in VALID_FINGERS:
        pose_set.add((finger, *EMERGENCY_THUMB_POSE))

    return sorted(
        pose_set,
        key=lambda item: (
            VALID_FINGERS.index(item[0]),
            item[1],
            item[2],
            item[3],
        ),
    )


def write_safe_thumb_poses(output_path, safe_poses):
    """Write the usable CSV format consumed by thumb clearance code."""
    with open(output_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["finger", "thumb_1", "thumb_2", "thumb_3"])

        for finger, thumb_1, thumb_2, thumb_3 in safe_poses:
            writer.writerow([finger, thumb_1, thumb_2, thumb_3])


def build_safe_thumb_poses_csv(
    input_file=DEFAULT_INPUT_FILE,
    output_file=DEFAULT_OUTPUT_FILE,
    include_emergency=False,
    use_exclusion_list=True,
):
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    safe_poses = load_safe_thumb_poses(
        input_path=input_path,
        use_exclusion_list=use_exclusion_list,
    )

    if include_emergency:
        safe_poses = add_emergency_pose(safe_poses)

    write_safe_thumb_poses(output_path, safe_poses)

    print(f"Read raw calibration file: {input_path}")
    print(f"Wrote usable safe thumb pose CSV: {output_path}")
    print(f"Safe poses written: {len(safe_poses)}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert raw thumb clearance calibration results into a usable safe-thumb-poses CSV."
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT_FILE,
        help=f"Raw calibration CSV. Default: {DEFAULT_INPUT_FILE}",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Clean output CSV. Default: {DEFAULT_OUTPUT_FILE}",
    )
    parser.add_argument(
        "--include-emergency",
        action="store_true",
        help="Add [0, 0, 0] as a safe emergency thumb pose for each finger.",
    )
    parser.add_argument(
        "--include-all-safe",
        action="store_true",
        help="Include every row marked s, without applying the cleaned-dataset exclusion list.",
    )

    args = parser.parse_args()

    build_safe_thumb_poses_csv(
        input_file=args.input,
        output_file=args.output,
        include_emergency=args.include_emergency,
        use_exclusion_list=not args.include_all_safe,
    )


if __name__ == "__main__":
    main()
