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

FINGERS = {
    "index": INDEX,
    "middle": MIDDLE,
    "ring": RING,
}

THUMB_1_VALUES = [0, 40, 80, 100]
THUMB_2_VALUES = [0, 40, 80, 100]
THUMB_3_VALUES = [0, 30, 60]

FINGER_OPEN = 0
FINGER_CLOSED = 80

RESULTS_FILE = "thumb_clearance_results.csv"


def make_pose(thumb_1, thumb_2, thumb_3, finger_name=None, finger_value=0):
    pose = [thumb_1, thumb_2, thumb_3, 0, 0, 0, 0]

    if finger_name is not None:
        finger_index = FINGERS[finger_name]
        pose[finger_index] = finger_value

    return pose


def load_completed_tests():
    completed_tests = set()

    if not os.path.exists(RESULTS_FILE):
        return completed_tests

    with open(RESULTS_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            thumb_1 = int(row["thumb_1"])
            thumb_2 = int(row["thumb_2"])
            thumb_3 = int(row["thumb_3"])
            finger = row["finger"]
            result = row["result"].strip().lower()

            if result in ["s", "u", "q"]:
                test_key = (thumb_1, thumb_2, thumb_3, finger)
                completed_tests.add(test_key)

    return completed_tests


def make_results_file_if_needed():
    if os.path.exists(RESULTS_FILE):
        return

    with open(RESULTS_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "thumb_1",
            "thumb_2",
            "thumb_3",
            "finger",
            "start_pose",
            "target_pose",
            "result"
        ])


def save_result(thumb_1, thumb_2, thumb_3, finger_name, start_pose, target_pose, result):


def make_pose(thumb_1, thumb_2, thumb_3, finger_name=None, finger_value=0):
    pose = [thumb_1, thumb_2, thumb_3, 0, 0, 0, 0]

    if finger_name is not None:
        finger_index = FINGERS[finger_name]
        pose[finger_index] = finger_value

    return pose


def load_completed_tests():
    """
    Reads the CSV file and remembers tests that already have a result.
    This lets you stop and restart without repeating everything.
    """

    completed_tests = set()

    if not os.path.exists(RESULTS_FILE):
        return completed_tests

    with open(RESULTS_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            thumb_1 = int(row["thumb_1"])
            thumb_2 = int(row["thumb_2"])
            thumb_3 = int(row["thumb_3"])
            finger = row["finger"]
            result = row["result"].strip().lower()

            if result in ["s", "u", "q"]:
                test_key = (thumb_1, thumb_2, thumb_3, finger)
                completed_tests.add(test_key)

    return completed_tests


def make_results_file_if_needed():
    """
    Creates the CSV file with a header if it does not already exist.
    """

    if os.path.exists(RESULTS_FILE):
        return

    with open(RESULTS_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "thumb_1",
            "thumb_2",
            "thumb_3",
            "finger",
            "start_pose",
            "target_pose",
            "result"
        ])


def save_result(thumb_1, thumb_2, thumb_3, finger_name, start_pose, target_pose, result):
    """
    Appends one result immediately so progress is not lost.
    """

    with open(RESULTS_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            thumb_1,
            thumb_2,
            thumb_3,
            finger_name,
            start_pose,
            target_pose,
            result
        ])

        file.flush()


def ask_before_running():
    """
    Lets you stop before the robot moves.
    This is safer than only asking after movement.
    """

    while True:
        answer = input("Run this test? [Enter=run, s=skip, x=stop]: ").lower().strip()

        if answer == "":
            return "run"

        if answer in ["s", "x"]:
            return answer

        print("Please press Enter, or type s, or x.")


def ask_result():
    while True:
        result = input("Result? [s=safe, u=unsafe, q=questionable, x=stop]: ").lower().strip()

        if result in ["s", "u", "q", "x"]:
            return result

        print("Please enter s, u, q, or x.")


def run_calibration():
    hand = AeroHand()

    make_results_file_if_needed()
    completed_tests = load_completed_tests()

    print(f"Loaded {len(completed_tests)} completed tests.")
    print("Already completed tests will be skipped.")

    try:
        for thumb_1 in THUMB_1_VALUES:
            for thumb_2 in THUMB_2_VALUES:
                for thumb_3 in THUMB_3_VALUES:
                    for finger_name in FINGERS:
                        test_key = (thumb_1, thumb_2, thumb_3, finger_name)

                        if test_key in completed_tests:
                            print(f"Skipping already completed test: {test_key}")
                            continue

                        print("\n--------------------------------")
                        print(f"Testing thumb: [{thumb_1}, {thumb_2}, {thumb_3}]")
                        print(f"Testing finger: {finger_name}")

                        start_pose = make_pose(
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            finger_name=None
                        )

                        target_pose = make_pose(
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            finger_name=finger_name,
                            finger_value=FINGER_CLOSED
                        )

                        trajectory = [
                            (OPEN_PALM, 1.0),
                            (start_pose, 1.0),
                            (target_pose, 1.0),
                            (start_pose, 1.0),
                            (OPEN_PALM, 1.0),
                        ]

                        print("Start pose:", start_pose)
                        print("Target pose:", target_pose)

                        decision = ask_before_running()

                        if decision == "x":
                            print("Stopping calibration before running test.")
                            return

                        if decision == "s":
                            save_result(
                                    thumb_1,
                                    thumb_2,
                                    thumb_3,
                                    finger_name,
                                    start_pose,
                                    target_pose,
                                    "q"
                                )
                            print("Skipped.")
                            continue

                        try:
                            hand.run_trajectory(trajectory)
                        except Exception as error:
                            print("Robot command failed:")
                            print(error)

                            result = input("Record this as questionable? [y/n/x]: ").lower().strip()

                            if result == "x":
                                print("Stopping calibration.")
                                return

                            if result == "y":
                                save_result(
                                    thumb_1,
                                    thumb_2,
                                    thumb_3,
                                    finger_name,
                                    start_pose,
                                    target_pose,
                                    "q"
                                )
                                completed_tests.add(test_key)

                            continue

                        result = ask_result()

                        if result == "x":
                            print("Stopping calibration.")
                            return

                        save_result(
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            finger_name,
                            start_pose,
                            target_pose,
                            result
                        )

                        completed_tests.add(test_key)
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

FINGERS = {
    "index": INDEX,
    "middle": MIDDLE,
    "ring": RING,
    # I would leave pinky out for now unless you really need it.
    # "pinky": PINKY,
}

THUMB_1_VALUES = [0, 40, 80, 100]
THUMB_2_VALUES = [0, 40, 80, 100]
THUMB_3_VALUES = [0, 30, 60]

FINGER_OPEN = 0
FINGER_CLOSED = 80

RESULTS_FILE = "thumb_clearance_results.csv"


def make_pose(thumb_1, thumb_2, thumb_3, finger_name=None, finger_value=0):
    pose = [thumb_1, thumb_2, thumb_3, 0, 0, 0, 0]

    if finger_name is not None:
        finger_index = FINGERS[finger_name]
        pose[finger_index] = finger_value

    return pose


def load_completed_tests():
    """
    Reads the CSV file and remembers tests that already have a result.
    This lets you stop and restart without repeating everything.
    """

    completed_tests = set()

    if not os.path.exists(RESULTS_FILE):
        return completed_tests

    with open(RESULTS_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            thumb_1 = int(row["thumb_1"])
            thumb_2 = int(row["thumb_2"])
            thumb_3 = int(row["thumb_3"])
            finger = row["finger"]
            result = row["result"].strip().lower()

            if result in ["s", "u", "q"]:
                test_key = (thumb_1, thumb_2, thumb_3, finger)
                completed_tests.add(test_key)

    return completed_tests


def make_results_file_if_needed():
    """
    Creates the CSV file with a header if it does not already exist.
    """

    if os.path.exists(RESULTS_FILE):
        return

    with open(RESULTS_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "thumb_1",
            "thumb_2",
            "thumb_3",
            "finger",
            "start_pose",
            "target_pose",
            "result"
        ])


def save_result(thumb_1, thumb_2, thumb_3, finger_name, start_pose, target_pose, result):
    """
    Appends one result immediately so progress is not lost.
    """

    with open(RESULTS_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            thumb_1,
            thumb_2,
            thumb_3,
            finger_name,
            start_pose,
            target_pose,
            result
        ])

        file.flush()


def ask_before_running():
    """
    Lets you stop before the robot moves.
    This is safer than only asking after movement.
    """

    while True:
        answer = input("Run this test? [Enter=run, s=skip, x=stop]: ").lower().strip()

        if answer == "":
            return "run"

        if answer in ["s", "x"]:
            return answer

        print("Please press Enter, or type s, or x.")


def ask_result():
    while True:
        result = input("Result? [s=safe, u=unsafe, q=questionable, x=stop]: ").lower().strip()

        if result in ["s", "u", "q", "x"]:
            return result

        print("Please enter s, u, q, or x.")


def run_calibration():
    hand = AeroHand()

    make_results_file_if_needed()
    completed_tests = load_completed_tests()

    print(f"Loaded {len(completed_tests)} completed tests.")
    print("Already completed tests will be skipped.")

    try:
        for thumb_1 in THUMB_1_VALUES:
            for thumb_2 in THUMB_2_VALUES:
                for thumb_3 in THUMB_3_VALUES:
                    for finger_name in FINGERS:
                        test_key = (thumb_1, thumb_2, thumb_3, finger_name)

                        if test_key in completed_tests:
                            print(f"Skipping already completed test: {test_key}")
                            continue

                        print("\n--------------------------------")
                        print(f"Testing thumb: [{thumb_1}, {thumb_2}, {thumb_3}]")
                        print(f"Testing finger: {finger_name}")

                        start_pose = make_pose(
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            finger_name=None
                        )

                        target_pose = make_pose(
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            finger_name=finger_name,
                            finger_value=FINGER_CLOSED
                        )

                        trajectory = [
                            (OPEN_PALM, 1.0),
                            (start_pose, 1.0),
                            (target_pose, 1.0),
                            (start_pose, 1.0),
                            (OPEN_PALM, 1.0),
                        ]

                        print("Start pose:", start_pose)
                        print("Target pose:", target_pose)

                        decision = ask_before_running()

                        if decision == "x":
                            print("Stopping calibration before running test.")
                            return

                        if decision == "s":
                            save_result(
                                    thumb_1,
                                    thumb_2,
                                    thumb_3,
                                    finger_name,
                                    start_pose,
                                    target_pose,
                                    "q"
                                )
                            print("Skipped.")
                            continue

                        try:
                            hand.run_trajectory(trajectory)
                        except Exception as error:
                            print("Robot command failed:")
                            print(error)

                            result = input("Record this as questionable? [y/n/x]: ").lower().strip()

                            if result == "x":
                                print("Stopping calibration.")
                                return

                            if result == "y":
                                save_result(
                                    thumb_1,
                                    thumb_2,
                                    thumb_3,
                                    finger_name,
                                    start_pose,
                                    target_pose,
                                    "q"
                                )
                                completed_tests.add(test_key)

                            continue

                        result = ask_result()

                        if result == "x":
                            print("Stopping calibration.")
                            return

                        save_result(
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            finger_name,
                            start_pose,
                            target_pose,
                            result
                        )

                        completed_tests.add(test_key)

    except KeyboardInterrupt:
        print("\nStopped with Ctrl+C. Saved results are still in the CSV file.")


if __name__ == "__main__":
    run_calibration()
    except KeyboardInterrupt:
        print("\nStopped with Ctrl+C. Saved results are still in the CSV file.")


if __name__ == "__main__":
    run_calibration()
    with open(RESULTS_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            thumb_1,
            thumb_2,
            thumb_3,
            finger_name,
            start_pose,
            target_pose,
            result
        ])

        file.flush()


def ask_before_running():
    """
    Lets you stop before the robot moves.
    This is safer than only asking after movement.
    """

    while True:
        answer = input("Run this test? [Enter=run, s=skip, x=stop]: ").lower().strip()

        if answer == "":
            return "run"

        if answer in ["s", "x"]:
            return answer

        print("Please press Enter, or type s, or x.")


def ask_result():
    while True:
        result = input("Result? [s=safe, u=unsafe, q=questionable, x=stop]: ").lower().strip()

        if result in ["s", "u", "q", "x"]:
            return result

        print("Please enter s, u, q, or x.")


def run_calibration():
    hand = AeroHand()

    make_results_file_if_needed()
    completed_tests = load_completed_tests()

    print(f"Loaded {len(completed_tests)} completed tests.")
    print("Already completed tests will be skipped.")

    try:
        for thumb_1 in THUMB_1_VALUES:
            for thumb_2 in THUMB_2_VALUES:
                for thumb_3 in THUMB_3_VALUES:
                    for finger_name in FINGERS:
                        test_key = (thumb_1, thumb_2, thumb_3, finger_name)

                        if test_key in completed_tests:
                            print(f"Skipping already completed test: {test_key}")
                            continue

                        print("\n--------------------------------")
                        print(f"Testing thumb: [{thumb_1}, {thumb_2}, {thumb_3}]")
                        print(f"Testing finger: {finger_name}")

                        start_pose = make_pose(
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            finger_name=None
                        )

                        target_pose = make_pose(
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            finger_name=finger_name,
                            finger_value=FINGER_CLOSED
                        )

                        trajectory = [
                            (OPEN_PALM, 1.0),
                            (start_pose, 1.0),
                            (target_pose, 1.0),
                            (start_pose, 1.0),
                            (OPEN_PALM, 1.0),
                        ]

                        print("Start pose:", start_pose)
                        print("Target pose:", target_pose)

                        decision = ask_before_running()

                        if decision == "x":
                            print("Stopping calibration before running test.")
                            return

                        if decision == "s":
                            save_result(
                                    thumb_1,
                                    thumb_2,
                                    thumb_3,
                                    finger_name,
                                    start_pose,
                                    target_pose,
                                    "q"
                                )
                            print("Skipped.")
                            continue

                        try:
                            hand.run_trajectory(trajectory)
                        except Exception as error:
                            print("Robot command failed:")
                            print(error)

                            result = input("Record this as questionable? [y/n/x]: ").lower().strip()

                            if result == "x":
                                print("Stopping calibration.")
                                return

                            if result == "y":
                                save_result(
                                    thumb_1,
                                    thumb_2,
                                    thumb_3,
                                    finger_name,
                                    start_pose,
                                    target_pose,
                                    "q"
                                )
                                completed_tests.add(test_key)

                            continue

                        result = ask_result()

                        if result == "x":
                            print("Stopping calibration.")
                            return

                        save_result(
                            thumb_1,
                            thumb_2,
                            thumb_3,
                            finger_name,
                            start_pose,
                            target_pose,
                            result
                        )

                        completed_tests.add(test_key)

    except KeyboardInterrupt:
        print("\nStopped with Ctrl+C. Saved results are still in the CSV file.")


if __name__ == "__main__":
    run_calibration()