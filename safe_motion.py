from calibration.calibration_data import (
    SAFE_THUMB_POSES,
    EMERGENCY_THUMB_CLEARANCE,
    FINGER_CLEARANCE_VALUES,
)

from pose_math import (
    THUMB_1,
    THUMB_2,
    THUMB_3,
    INDEX,
    MIDDLE,
    RING,
    PINKY,
    FINGER_JOINTS,
    get_thumb_pose,
    get_moving_fingers,
    thumb_is_moving,
    both_thumb_and_fingers_are_moving,
    score_thumb_pose,
)


MIN_VALUE = 0
MAX_VALUE = 100

OPEN_PALM = [0, 0, 0, 0, 0, 0, 0]

DEFAULT_CLEARANCE_TIME = 0.5

FINGER_NAMES = {
    INDEX: "index",
    MIDDLE: "middle",
    RING: "ring",
}


# ------------------------------------------------------------
# Basic validation
# ------------------------------------------------------------

def validate_pose(pose):
    if len(pose) != 7:
        raise ValueError("Pose must contain exactly 7 values.")

    for value in pose:
        if not isinstance(value, (int, float)):
            raise TypeError("Pose values must be numeric.")

    return True


def constrain_pose(pose):
    validate_pose(pose)

    constrained_pose = []

    for value in pose:
        if value < MIN_VALUE:
            constrained_value = MIN_VALUE
        elif value > MAX_VALUE:
            constrained_value = MAX_VALUE
        else:
            constrained_value = value

        constrained_pose.append(constrained_value)

    return constrained_pose


def sanitize_trajectory(raw_trajectory):
    sanitized_trajectory = []

    for pose, duration in raw_trajectory:
        constrained_pose = constrain_pose(pose)
        sanitized_trajectory.append((constrained_pose, duration))

    return sanitized_trajectory


# ------------------------------------------------------------
# Finger clearance / release
# ------------------------------------------------------------

def get_blocking_fingers(pose):
    blocking_fingers = []

    for finger_index in FINGER_JOINTS:
        clearance_value = FINGER_CLEARANCE_VALUES[finger_index]

        if pose[finger_index] > clearance_value:
            blocking_fingers.append(finger_index)

    return blocking_fingers


def fingers_are_in_conflict_zone(pose):
    return len(get_blocking_fingers(pose)) > 0


def fingers_are_opening(start_pose, target_pose):
    """
    Returns True if index, middle, or ring are moving toward open.
    Since 0 is open, opening means target value is smaller.
    """

    for finger_index in FINGER_JOINTS:
        if target_pose[finger_index] < start_pose[finger_index]:
            return True

    return False


def make_finger_clearance_pose(start_pose, blocking_fingers):
    """
    Moves blocking fingers to their tested clearance values.
    This does not fully open them.
    """

    clearance_pose = start_pose.copy()

    for finger_index in blocking_fingers:
        clearance_pose[finger_index] = FINGER_CLEARANCE_VALUES[finger_index]

    return clearance_pose


def make_full_finger_release_pose(start_pose):
    """
    Fully opens index, middle, ring, and pinky.
    Pinky is not used for thumb safety calibration,
    but it should move with the rest of the hand during a full release.
    """

    release_pose = start_pose.copy()

    release_pose[INDEX] = 0
    release_pose[MIDDLE] = 0
    release_pose[RING] = 0
    release_pose[PINKY] = 0

    return release_pose


def make_finger_target_pose(start_pose, target_pose):
    """
    Moves fingers to the target finger values while keeping the thumb unchanged.
    Includes pinky because this is about forming the target handshape.
    """

    finger_target_pose = start_pose.copy()

    finger_target_pose[INDEX] = target_pose[INDEX]
    finger_target_pose[MIDDLE] = target_pose[MIDDLE]
    finger_target_pose[RING] = target_pose[RING]
    finger_target_pose[PINKY] = target_pose[PINKY]

    return finger_target_pose


# ------------------------------------------------------------
# Thumb movement
# ------------------------------------------------------------

def make_thumb_target_pose(start_pose, target_pose):
    """
    Moves only the thumb to the target thumb position.
    Fingers stay where they are.
    """

    thumb_target_pose = start_pose.copy()

    thumb_target_pose[THUMB_1] = target_pose[THUMB_1]
    thumb_target_pose[THUMB_2] = target_pose[THUMB_2]
    thumb_target_pose[THUMB_3] = target_pose[THUMB_3]

    return thumb_target_pose


def make_thumb_out_pose(start_pose):
    """
    Moves only the thumb to the emergency/out-of-way position.
    Fingers stay where they are.
    """

    thumb_out_pose = start_pose.copy()

    thumb_out_pose[THUMB_1] = EMERGENCY_THUMB_CLEARANCE[0]
    thumb_out_pose[THUMB_2] = EMERGENCY_THUMB_CLEARANCE[1]
    thumb_out_pose[THUMB_3] = EMERGENCY_THUMB_CLEARANCE[2]

    return thumb_out_pose


# ------------------------------------------------------------
# Calibrated thumb clearance
# ------------------------------------------------------------

def find_common_safe_thumb_poses(moving_fingers):
    common_poses = None

    for finger_index in moving_fingers:
        finger_name = FINGER_NAMES[finger_index]

        if finger_name not in SAFE_THUMB_POSES:
            continue

        finger_pose_set = set()

        for pose in SAFE_THUMB_POSES[finger_name]:
            finger_pose_set.add(tuple(pose))

        if common_poses is None:
            common_poses = finger_pose_set
        else:
            common_poses = common_poses.intersection(finger_pose_set)

    if common_poses is None:
        return []

    common_pose_list = []

    for pose_tuple in common_poses:
        common_pose_list.append(list(pose_tuple))

    return common_pose_list


def find_best_safe_thumb_pose(current_thumb_pose, moving_fingers):
    common_safe_poses = find_common_safe_thumb_poses(moving_fingers)

    if len(common_safe_poses) == 0:
        return EMERGENCY_THUMB_CLEARANCE

    best_pose = common_safe_poses[0]
    best_score = score_thumb_pose(current_thumb_pose, best_pose)

    for candidate_pose in common_safe_poses:
        candidate_score = score_thumb_pose(
            current_thumb_pose,
            candidate_pose
        )

        if candidate_score < best_score:
            best_pose = candidate_pose
            best_score = candidate_score

    return best_pose


def make_thumb_clearance_pose(start_pose, moving_fingers):
    """
    Moves the thumb to the closest calibrated safe pose
    for the fingers that are moving.
    """

    clearance_pose = start_pose.copy()

    if len(moving_fingers) == 0:
        return clearance_pose

    current_thumb_pose = get_thumb_pose(start_pose)

    safe_thumb_pose = find_best_safe_thumb_pose(
        current_thumb_pose=current_thumb_pose,
        moving_fingers=moving_fingers
    )

    clearance_pose[THUMB_1] = safe_thumb_pose[0]
    clearance_pose[THUMB_2] = safe_thumb_pose[1]
    clearance_pose[THUMB_3] = safe_thumb_pose[2]

    return clearance_pose


# ------------------------------------------------------------
# Thumb/finger relationship classification
# ------------------------------------------------------------

def get_finger_context(pose):
    index = pose[INDEX]
    middle = pose[MIDDLE]
    ring = pose[RING]
    pinky = pose[PINKY]

    if index <= 54 and middle <= 54 and ring <= 54:
        return "clearance"

    if index >= 85 and middle >= 85 and ring >= 85 and pinky <= 20:
        return "i_like"

    if index >= 75 and middle >= 75 and ring >= 75 and pinky >= 75:
        return "s_like"

    if 50 <= index <= 70 and 50 <= middle <= 70 and 50 <= ring <= 70:
        return "m_like"

    return "unknown"


def get_thumb_relation(pose):
    """
    Approximate thumb relationship based on calibrated patterns.

    Returns:
    - "under"
    - "over"
    - "neutral"
    - "collision"
    - "unknown"
    """

    thumb_1 = pose[THUMB_1]
    thumb_2 = pose[THUMB_2]
    thumb_3 = pose[THUMB_3]

    context = get_finger_context(pose)

    if context == "clearance":
        # B-like thumb-under position:
        # [20, 100, 70, 0, 0, 0, 0]
        if thumb_2 >= 90 and thumb_3 >= 55:
            return "under"

        if thumb_3 >= 55:
            return "under"

        if thumb_3 <= 35 and thumb_2 >= 80:
            return "collision"

        if thumb_1 <= 45 and thumb_2 <= 45 and thumb_3 <= 35:
            return "neutral"

        return "unknown"

    if context == "m_like":
        # Catches your actual M pose:
        # [100, 100, 40, 60, 60, 60, 60]
        if thumb_2 >= 90 and thumb_3 >= 40:
            return "under"

        if thumb_3 >= 55:
            return "under"

        if thumb_3 <= 35 and thumb_2 >= 90:
            return "collision"

        if thumb_1 >= 75 and thumb_2 <= 85 and thumb_3 <= 35:
            return "over"

        if thumb_1 <= 45 and thumb_2 <= 45 and thumb_3 <= 35:
            return "neutral"

        return "unknown"

    if context == "i_like":
        if thumb_1 >= 75 and thumb_3 <= 65:
            return "over"

        if thumb_1 <= 45 and thumb_2 <= 45 and thumb_3 <= 35:
            return "neutral"

        if thumb_1 <= 45 and thumb_3 >= 55:
            return "collision"

        return "unknown"

    if context == "s_like":
        if thumb_1 >= 75 and thumb_2 <= 85:
            return "over"

        if thumb_1 <= 45 and thumb_2 <= 45 and thumb_3 <= 35:
            return "neutral"

        if thumb_2 >= 100 or thumb_3 >= 60:
            return "collision"

        return "unknown"

    return "unknown"


def is_under_to_over_transition(start_pose, target_pose):
    start_relation = get_thumb_relation(start_pose)
    target_relation = get_thumb_relation(target_pose)

    return start_relation == "under" and target_relation == "over"


def is_over_to_under_transition(start_pose, target_pose):
    start_relation = get_thumb_relation(start_pose)
    target_relation = get_thumb_relation(target_pose)

    return start_relation == "over" and target_relation == "under"


# ------------------------------------------------------------
# Special transition resolvers
# ------------------------------------------------------------

def resolve_under_to_over_transition(start_pose, target_pose, duration):
    """
    Example: M-like/B-like shape to I/S-like shape.

    Safer order:
    1. Move fingers to clearance values.
    2. Move thumb to calibrated safe clearance.
    3. Move to target.
    """

    resolved_steps = []

    blocking_fingers = get_blocking_fingers(start_pose)

    if len(blocking_fingers) > 0:
        finger_clearance_pose = make_finger_clearance_pose(
            start_pose=start_pose,
            blocking_fingers=blocking_fingers
        )

        if finger_clearance_pose != start_pose:
            resolved_steps.append((finger_clearance_pose, DEFAULT_CLEARANCE_TIME))
            start_pose = finger_clearance_pose

    moving_fingers = get_moving_fingers(start_pose, target_pose)

    if len(moving_fingers) > 0:
        thumb_clearance_pose = make_thumb_clearance_pose(
            start_pose=start_pose,
            moving_fingers=moving_fingers
        )

        if thumb_clearance_pose != start_pose:
            resolved_steps.append((thumb_clearance_pose, DEFAULT_CLEARANCE_TIME))
            start_pose = thumb_clearance_pose

    resolved_steps.append((target_pose, duration))
    return resolved_steps


def resolve_over_to_under_transition(start_pose, target_pose, duration):
    """
    Example: S/I-like shape to B/M/N-like shape.

    Safer order:
    1. Move thumb out.
    2. Release fingers.
    3. Move thumb toward target.
    4. Move to final target.
    """

    resolved_steps = []

    thumb_out_pose = make_thumb_out_pose(start_pose)

    if thumb_out_pose != start_pose:
        resolved_steps.append((thumb_out_pose, DEFAULT_CLEARANCE_TIME))
        start_pose = thumb_out_pose

    finger_release_pose = make_full_finger_release_pose(start_pose)

    if finger_release_pose != start_pose:
        resolved_steps.append((finger_release_pose, DEFAULT_CLEARANCE_TIME))
        start_pose = finger_release_pose

    thumb_target_pose = make_thumb_target_pose(
        start_pose=start_pose,
        target_pose=target_pose
    )

    if thumb_target_pose != start_pose:
        resolved_steps.append((thumb_target_pose, DEFAULT_CLEARANCE_TIME))
        start_pose = thumb_target_pose

    resolved_steps.append((target_pose, duration))
    return resolved_steps


def resolve_over_to_open_fingers_transition(start_pose, target_pose, duration):
    """
    Handles cases where thumb is over/across the fingers and fingers need to open,
    but the target is not classified as under.

    Example:
    S-like pose to a non-under open-finger pose.

    Safer order:
    1. Move thumb out first.
    2. Move fingers to target.
    3. Move thumb to target.
    4. Finish target.
    """

    resolved_steps = []

    thumb_out_pose = make_thumb_out_pose(start_pose)

    if thumb_out_pose != start_pose:
        resolved_steps.append((thumb_out_pose, DEFAULT_CLEARANCE_TIME))
        start_pose = thumb_out_pose

    finger_target_pose = make_finger_target_pose(
        start_pose=start_pose,
        target_pose=target_pose
    )

    if finger_target_pose != start_pose:
        resolved_steps.append((finger_target_pose, DEFAULT_CLEARANCE_TIME))
        start_pose = finger_target_pose

    thumb_target_pose = make_thumb_target_pose(
        start_pose=start_pose,
        target_pose=target_pose
    )

    if thumb_target_pose != start_pose:
        resolved_steps.append((thumb_target_pose, DEFAULT_CLEARANCE_TIME))
        start_pose = thumb_target_pose

    resolved_steps.append((target_pose, duration))
    return resolved_steps


def resolve_open_palm_transition(start_pose, duration):
    """
    Returning to open palm depends on thumb relation.

    under -> open:
        fully release fingers first, then thumb out, then open

    over/neutral/unknown -> open:
        thumb out first, then open
    """

    resolved_steps = []
    relation = get_thumb_relation(start_pose)

    if relation == "under":
        finger_release_pose = make_full_finger_release_pose(start_pose)

        if finger_release_pose != start_pose:
            resolved_steps.append((finger_release_pose, DEFAULT_CLEARANCE_TIME))
            start_pose = finger_release_pose

        thumb_out_pose = make_thumb_out_pose(start_pose)

        if thumb_out_pose != start_pose:
            resolved_steps.append((thumb_out_pose, DEFAULT_CLEARANCE_TIME))
            start_pose = thumb_out_pose

        resolved_steps.append((OPEN_PALM, duration))
        return resolved_steps

    thumb_out_pose = make_thumb_out_pose(start_pose)

    if thumb_out_pose != start_pose:
        resolved_steps.append((thumb_out_pose, DEFAULT_CLEARANCE_TIME))
        start_pose = thumb_out_pose

    resolved_steps.append((OPEN_PALM, duration))
    return resolved_steps


# ------------------------------------------------------------
# Main transition resolver
# ------------------------------------------------------------

def resolve_transition(start_pose, target_pose, duration):
    resolved_steps = []

    if target_pose == OPEN_PALM:
        return resolve_open_palm_transition(
            start_pose=start_pose,
            duration=duration
        )

    # Important: check true relationship transitions first.
    # This lets B count as an under-target before the over-to-open rule catches it.
    if is_under_to_over_transition(start_pose, target_pose):
        return resolve_under_to_over_transition(
            start_pose=start_pose,
            target_pose=target_pose,
            duration=duration
        )

    if is_over_to_under_transition(start_pose, target_pose):
        return resolve_over_to_under_transition(
            start_pose=start_pose,
            target_pose=target_pose,
            duration=duration
        )

    start_relation = get_thumb_relation(start_pose)

    # Over-thumb pose to a pose where fingers need to open, but not an under-target.
    if start_relation == "over" and fingers_are_opening(start_pose, target_pose):
        return resolve_over_to_open_fingers_transition(
            start_pose=start_pose,
            target_pose=target_pose,
            duration=duration
        )

    # General case:
    # If thumb and index/middle/ring are both moving,
    # split the motion so they do not move together.
    if both_thumb_and_fingers_are_moving(start_pose, target_pose):
        if fingers_are_in_conflict_zone(start_pose):
            blocking_fingers = get_blocking_fingers(start_pose)

            finger_clearance_pose = make_finger_clearance_pose(
                start_pose=start_pose,
                blocking_fingers=blocking_fingers
            )

            if finger_clearance_pose != start_pose:
                resolved_steps.append((finger_clearance_pose, DEFAULT_CLEARANCE_TIME))
                start_pose = finger_clearance_pose

        thumb_target_pose = make_thumb_target_pose(
            start_pose=start_pose,
            target_pose=target_pose
        )

        if thumb_target_pose != start_pose:
            resolved_steps.append((thumb_target_pose, DEFAULT_CLEARANCE_TIME))
            start_pose = thumb_target_pose

        resolved_steps.append((target_pose, duration))
        return resolved_steps

    # Thumb-only case:
    if thumb_is_moving(start_pose, target_pose):
        blocking_fingers = get_blocking_fingers(start_pose)

        if len(blocking_fingers) > 0:
            finger_clearance_pose = make_finger_clearance_pose(
                start_pose=start_pose,
                blocking_fingers=blocking_fingers
            )

            if finger_clearance_pose != start_pose:
                resolved_steps.append((finger_clearance_pose, DEFAULT_CLEARANCE_TIME))
                start_pose = finger_clearance_pose

        thumb_target_pose = make_thumb_target_pose(
            start_pose=start_pose,
            target_pose=target_pose
        )

        if thumb_target_pose != start_pose:
            resolved_steps.append((thumb_target_pose, DEFAULT_CLEARANCE_TIME))
            start_pose = thumb_target_pose

        resolved_steps.append((target_pose, duration))
        return resolved_steps

    # Finger-only case:
    # Do not automatically move the thumb when only fingers are moving.
    # Letter sequences are responsible for thumb/finger ordering.
    resolved_steps.append((target_pose, duration))
    return resolved_steps


def make_trajectory_safe(raw_trajectory):
    raw_trajectory = sanitize_trajectory(raw_trajectory)

    if len(raw_trajectory) <= 1:
        return raw_trajectory

    safe_trajectory = [raw_trajectory[0]]

    for i in range(1, len(raw_trajectory)):
        start_pose = safe_trajectory[-1][0]
        target_pose, duration = raw_trajectory[i]

        resolved_steps = resolve_transition(
            start_pose=start_pose,
            target_pose=target_pose,
            duration=duration
        )

        for step in resolved_steps:
            safe_trajectory.append(step)

    return safe_trajectory