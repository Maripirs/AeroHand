
THUMB_1 = 0
THUMB_2 = 1
THUMB_3 = 2

INDEX = 3
MIDDLE = 4
RING = 5
PINKY = 6

THUMB_JOINTS = [THUMB_1, THUMB_2, THUMB_3]
FINGER_JOINTS = [INDEX, MIDDLE, RING]


def get_thumb_pose(pose):
    return [
        pose[THUMB_1],
        pose[THUMB_2],
        pose[THUMB_3],
    ]


def get_moving_fingers(start_pose, target_pose):
    moving_fingers = []

    for finger_index in FINGER_JOINTS:
        if start_pose[finger_index] != target_pose[finger_index]:
            moving_fingers.append(finger_index)

    return moving_fingers


def thumb_is_moving(start_pose, target_pose):
    for thumb_index in THUMB_JOINTS:
        if start_pose[thumb_index] != target_pose[thumb_index]:
            return True

    return False


def both_thumb_and_fingers_are_moving(start_pose, target_pose):
    if not thumb_is_moving(start_pose, target_pose):
        return False

    moving_fingers = get_moving_fingers(start_pose, target_pose)

    if len(moving_fingers) == 0:
        return False

    return True


def count_changed_axes(current_thumb_pose, candidate_thumb_pose):
    changed_axes = 0

    for i in range(3):
        if current_thumb_pose[i] != candidate_thumb_pose[i]:
            changed_axes += 1

    return changed_axes


def thumb_distance(current_thumb_pose, candidate_thumb_pose):
    total = 0

    for i in range(3):
        difference = current_thumb_pose[i] - candidate_thumb_pose[i]
        total += difference * difference

    return total


def score_thumb_pose(current_thumb_pose, candidate_thumb_pose):
    """
    Lower score is better:
    1. Change fewer thumb axes.
    2. Move a shorter total distance.
    """

    changed_axes = count_changed_axes(
        current_thumb_pose,
        candidate_thumb_pose
    )

    distance = thumb_distance(
        current_thumb_pose,
        candidate_thumb_pose
    )

    return changed_axes, distance