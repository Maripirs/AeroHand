from aero_open_sdk.aero_hand import AeroHand

from projects.asl_alphabet.asl_alphabet import ASL_ALPHABET

from safe_motion import (
    resolve_transition,
    make_trajectory_safe,
)


OPEN_PALM = [0, 0, 0, 0, 0, 0, 0]

START_TIME = 1.0
MOVE_TIME = 0.5
HOLD_TIME = 3
END_TIME = 1.0


def clean_letter_sequence(user_input):

    letters = []

    for character in user_input.upper():
        if character == " ":
            continue

        if character in ASL_ALPHABET:
            letters.append(character)
        else:
            print(f"Skipping unsupported character: {character}")

    return letters


def apply_partial_step(current_pose, step):

    next_pose = current_pose.copy()

    for joint_index, joint_value in step["set"].items():
        next_pose[joint_index] = joint_value

    duration = step.get("duration", MOVE_TIME)

    return next_pose, duration


def add_safe_transition(trajectory, next_pose, duration):

    if len(trajectory) == 0:
        trajectory.append((next_pose, duration))
        return

    start_pose = trajectory[-1][0]

    transition_steps = resolve_transition(
        start_pose=start_pose,
        target_pose=next_pose,
        duration=duration
    )

    for step in transition_steps:
        trajectory.append(step)


def add_letter_to_trajectory(trajectory, letter):

    letter_data = ASL_ALPHABET[letter]

    print()
    print(f"Letter: {letter}")
    print(letter_data)
    # print(f"Status: {letter_data.get('status', 'unknown')}")
    # print(f"Status: {letter_data.get('status', 'unknown')}")
    # print(f"Notes: {letter_data.get('notes', 'No notes')}")

    sequence = letter_data.get("sequence")

    if sequence is not None:
        for step_index, step in enumerate(sequence):
            current_pose = trajectory[-1][0]
            next_pose, duration = apply_partial_step(current_pose, step)

            if step_index == 0:
                add_safe_transition(
                    trajectory=trajectory,
                    next_pose=next_pose,
                    duration=duration
                )
            else:
                trajectory.append((next_pose, duration))

        trajectory.append((trajectory[-1][0], HOLD_TIME))
        return

    target_pose = letter_data["pose"]

    add_safe_transition(
        trajectory=trajectory,
        next_pose=target_pose,
        duration=MOVE_TIME
    )

    trajectory.append((target_pose, HOLD_TIME))


def build_sequence_trajectory(letters):

    trajectory = [(OPEN_PALM, START_TIME)]

    for letter in letters:
        add_letter_to_trajectory(trajectory, letter)

    add_safe_transition(
        trajectory=trajectory,
        next_pose=OPEN_PALM,
        duration=END_TIME
    )

    return trajectory


def print_trajectory(title, trajectory):
    print()
    print(title)

    for pose, duration in trajectory:
        print(f"{pose}, {duration}")


def letter_sequence(hand):

    user_input = input("\nType a sequence of letters, or q to quit: ").strip()

    if user_input.lower() in ["q", "quit", "exit"]:
        return False

    letters = clean_letter_sequence(user_input)

    if len(letters) == 0:
        print("No supported letters entered.")
        return True

    final_trajectory = build_sequence_trajectory(letters)

    print_trajectory("Final safe trajectory:", final_trajectory)

    hand.run_trajectory(final_trajectory)


    return True


def test_clearance(hand):

    test_trajectory = [
        ([0, 0, 0, 0, 0, 0, 0], 1.0),
        ([100, 100, 40, 60, 60, 60, 60], 2.0),
        ([80, 40, 40, 90, 90, 90, 0], 2.0),
        ([0, 0, 0, 0, 0, 0, 0], 1.0),
    ]

    safe_trajectory = make_trajectory_safe(test_trajectory)

    print_trajectory("Final safe trajectory:", safe_trajectory)

    hand.run_trajectory(safe_trajectory)


def main():
    hand = AeroHand()
    letter_sequence(hand)


if __name__ == "__main__":
    main()