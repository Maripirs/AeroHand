# calibrate_thumb_relation.py

from aero_open_sdk.aero_hand import AeroHand
import csv
import os

OPEN_PALM = [0, 0, 0, 0, 0, 0, 0]

THUMB_1 = 0
THUMB_2 = 1
THUMB_3 = 2

INDEX = 3
MIDDLE = 4
RING = 5
PINKY = 6

THUMB_1_VALUES = [40, 80, 100]
THUMB_2_VALUES = [40, 80, 100]
THUMB_3_VALUES = [30, 60]

FINGER_CONTEXTS = {
    "clearance": {
        "values": [48, 49, 54, 0],
        "notes": "Index/middle/ring at tested clearance values.",
    },

    "m_like": {
        "values": [60, 60, 60, 60],
        "notes": "M-like curled fingers.",
    },

    "i_like": {
        "values": [90, 90, 90, 0],
        "notes": "I-like fingers: index/middle/ring curled, pinky open.",
    },

    "s_like": {
        "values": [80, 80, 80, 90],
        "notes": "S-like closed fist.",
    },
}

OUTPUT_FILE = "thumb_relation_map.csv"


def make_pose(thumb_1, thumb_2, thumb_3, finger_values):
    index = finger_values[0]
    middle = finger_values[1]
    ring = finger_values[2]
    pinky = finger_values[3]

    return [
        thumb_1,
        thumb_2,
        thumb_3,
        index,
        middle,
        ring,
        pinky,
    ]


def make_output_file_if_needed():
    if os.path.exists(OUTPUT_FILE):
        return

    with open(OUTPUT_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "thumb_1",
            "thumb_2",
            "thumb_3",
            "finger_context",
            "index",
            "middle",
            "ring",
            "pinky",
            "full_pose",
            "relation",
        ])


def load_completed_tests():
    completed_tests = set()

    if not os.path.exists(OUTPUT_FILE):
        return completed_tests

    with open(OUTPUT_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            thumb_1 = int(row["thumb_1"])
            thumb_2 = int(row["thumb_2"])
            thumb_3 = int(row["thumb_3"])
            finger_context = row["finger_context"]

            completed_tests.add((
                thumb_1,
                thumb_2,
                thumb_3,
                finger_context,
            ))

    return completed_tests


def save_result(
    thumb_1,
    thumb_2,
    thumb_3,
    finger_context,
    finger_values,
    full_pose,
    relation,

):
    with open(OUTPUT_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            thumb_1,
            thumb_2,
            thumb_3,
            finger_context,
            finger_values[0],
            finger_values[1],
            finger_values[2],
            finger_values[3],
            full_pose,
            relation,

        ])

        file.flush()


def ask_before_running():
    while True:
        answer = input("Run this test? [Enter=run, s=skip, x=stop]: ").lower().strip()

        if answer == "":
            return "run"

        if answer == "s":
            return "skip"

        if answer == "x":
            return "stop"

        print("Please press Enter, or type s, or x.")


def ask_relation():
    print()
    print("Relation labels:")
    print("u = thumb under fingers")
    print("o = thumb over/across fingers")
    print("n = neutral / out of the way")
    print("b = between fingers")
    print("c = collision / conflict")
    print("q = questionable / unclear")
    print("x = stop")

    while True:
        relation = input("Thumb relation? [u/o/n/b/c/q/x]: ").lower().strip()

        if relation in ["u", "o", "n", "b", "c", "q", "x"]:
            return relation

        print("Please enter u, o, n, b, c, q, or x.")


def relation_to_text(relation):
    if relation == "u":
        return "under"

    if relation == "o":
        return "over"

    if relation == "n":
        return "neutral"

    if relation == "b":
        return "between"

    if relation == "c":
        return "collision"

    if relation == "q":
        return "questionable"

    return relation


def run_calibration():
    hand = AeroHand()

    make_output_file_if_needed()
    completed_tests = load_completed_tests()

    print(f"Loaded {len(completed_tests)} completed tests.")
    print(f"Results will be saved to: {OUTPUT_FILE}")

    try:
        for context_name in FINGER_CONTEXTS:
            context_data = FINGER_CONTEXTS[context_name]
            finger_values = context_data["values"]
            context_notes = context_data["notes"]

            print()
            print("================================")
            print(f"Finger context: {context_name}")
            print(context_notes)
            print("================================")

            for thumb_1 in THUMB_1_VALUES:
                for thumb_2 in THUMB_2_VALUES:
                    for thumb_3 in THUMB_3_VALUES:
                        test_key = (
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            context_name,
                        )

                        if test_key in completed_tests:
                            print(f"Skipping completed test: {test_key}")
                            continue

                        pose = make_pose(
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            finger_values,
                        )

                        print()
                        print("--------------------------------")
                        print(f"Thumb pose: [{thumb_1}, {thumb_2}, {thumb_3}]")
                        print(f"Finger context: {context_name}")
                        print(f"Finger values: {finger_values}")
                        print(f"Full pose: {pose}")

                        decision = ask_before_running()

                        if decision == "stop":
                            print("Stopping before test.")
                            return

                        if decision == "skip":
                            print("Skipped. No result saved.")
                            continue

                        trajectory = [
                            (OPEN_PALM, 1.0),
                            (pose, 1.0),
                            (pose, 1.0),
                            (OPEN_PALM, 1.0),
                        ]

                        try:
                            hand.run_trajectory(trajectory)
                        except Exception as error:
                            print("Robot command failed:")
                            print(error)

                            mark_collision = input("Record as collision/conflict? [y/n/x]: ").lower().strip()

                            if mark_collision == "x":
                                print("Stopping.")
                                return

                            if mark_collision == "y":
                                save_result(
                                    thumb_1=thumb_1,
                                    thumb_2=thumb_2,
                                    thumb_3=thumb_3,
                                    finger_context=context_name,
                                    finger_values=finger_values,
                                    full_pose=pose,
                                    relation="collision",
                                    notes="Robot command failed or movement appeared unsafe.",
                                )
                                completed_tests.add(test_key)

                            continue

                        relation = ask_relation()

                        if relation == "x":
                            print("Stopping.")
                            return

                        relation_text = relation_to_text(relation)


                        save_result(
                            thumb_1=thumb_1,
                            thumb_2=thumb_2,
                            thumb_3=thumb_3,
                            finger_context=context_name,
                            finger_values=finger_values,
                            full_pose=pose,
                            relation=relation_text,

                        )

                        completed_tests.add(test_key)

    except KeyboardInterrupt:
        print()
        print("Stopped with Ctrl+C. Saved results remain in the CSV file.")


if __name__ == "__main__":
    run_calibration()