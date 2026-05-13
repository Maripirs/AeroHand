# AeroHand Safe Motion

This project is a safety-focused motion system for the AeroHand robotic hand. It builds safer hand trajectories by checking poses, using human-labeled calibration data, and inserting safer transition steps when the thumb and fingers could interfere with each other.

The project is not mainly a simulator project. The current demo code is set up to run on the physical `AeroHand`. The ASL handshape demo is included as a test application for the safe motion system.

## Core Idea

A hand pose is represented as a list of seven numeric values:

```text
[thumb_1, thumb_2, thumb_3, index, middle, ring, pinky]
```

The safety system assumes values should stay in the range `0` to `100`. Before a trajectory is used, poses are validated and constrained to that range.

The main safety problem this project handles is thumb/finger interference. Some thumb positions are safe when the fingers are open, but unsafe when the fingers close. Some transitions also need different ordering depending on whether the thumb is under, over, neutral, or in conflict with the fingers.

## Repository Files

| File | Purpose |
|---|---|
| `safe_motion.py` | Main safety transition resolver. Validates poses, constrains values, detects thumb/finger relationships, and inserts safer transition steps. |
| `pose_math.py` | Shared pose constants and helper functions for detecting moving joints, measuring thumb movement, and scoring candidate thumb poses. |
| `safety_calibration_data.py` | Hard-coded calibration data used by the safety system, including safe thumb poses, finger clearance values, and emergency thumb clearance. |
| `calibrate_thumb_clearance.py` | Human-in-the-loop calibration script for testing thumb clearance while one finger closes. Saves user-labeled results to `thumb_clearance_results.csv`. |
| `calibrate_thumb_relation.py` | Human-in-the-loop calibration script for labeling thumb position as under, over, neutral, between, collision, or questionable. Saves labels to `thumb_relation_map.csv`. |

## Calibration Data Files

| File | Purpose |
|---|---|
| `thumb_clearance_results.csv` | Raw human-labeled calibration results for thumb/finger clearance tests. |
| `safe_thumb_poses.csv` | Safe thumb poses derived from clearance testing. |
| `safe_thumb_poses_clean.csv` | Cleaned safe thumb pose list. |
| `thumb_relation_map.csv` | Human-labeled thumb relation data for different finger contexts. |

## Human-in-the-Loop Calibration

The calibration scripts do not automatically decide whether a pose is safe. They move the hand through a test pose and ask the user to label what happened.

This is intentional. The safety of a robotic hand pose depends on what the physical hand actually does, not only on the numeric values in the pose list.

### Thumb Clearance Calibration

`testThumb.py` tests thumb clearance while one finger moves.

For each test, the script:

1. Creates a thumb pose from tested thumb values.
2. Selects one finger: index, middle, or ring.
3. Builds a trajectory from open palm to the thumb pose, then closes that finger.
4. Asks the user whether to run, skip, or stop before the robot moves.
5. After movement, asks the user to label the result as safe, unsafe, questionable, or stop.
6. Saves each result immediately to `thumb_clearance_results.csv`.

The script also loads previously completed tests so calibration can be stopped and restarted without repeating every test.

### Thumb Relation Calibration

`thumb_relation.py` tests how the thumb sits relative to the fingers.

For each test, the script:

1. Selects a finger context such as `clearance`, `m_like`, `i_like`, or `s_like`.
2. Combines that finger context with a tested thumb pose.
3. Runs the pose on the hand after user confirmation.
4. Asks the user to label the thumb relation.
5. Saves the label to `thumb_relation_map.csv`.

The supported relation labels are:

| Input | Saved Label |
|---|---|
| `u` | `under` |
| `o` | `over` |
| `n` | `neutral` |
| `b` | `between` |
| `c` | `collision` |
| `q` | `questionable` |

## Safety Logic

The main safety logic lives in `safety.py`.

### Basic Pose Validation

Every pose must contain exactly seven numeric values. Values below `0` are constrained to `0`, and values above `100` are constrained to `100`.

### Finger Clearance

The safety system tracks the index, middle, and ring fingers for thumb clearance. A finger is treated as blocking if its value is above its tested clearance value.

Current clearance values:

```python
FINGER_CLEARANCE_VALUES = {
    3: 37,  # index
    4: 44,  # middle
    5: 49,  # ring
}
```

When needed, the system can move blocking fingers to their clearance values instead of fully opening them.

### Safe Thumb Clearance

When fingers are moving, the system looks for thumb poses that were labeled safe for all moving fingers. If more than one pose is safe, it chooses the closest one to the current thumb pose.

The scoring favors:

1. Changing fewer thumb axes.
2. Moving a shorter total distance.

If no common safe thumb pose exists, the system uses the emergency thumb clearance pose:

```python
EMERGENCY_THUMB_CLEARANCE = [0, 0, 0]
```

### Thumb/Finger Relationship

The safety system classifies the thumb relationship using finger context and thumb position. Possible classifications are:

- `under`
- `over`
- `neutral`
- `collision`
- `unknown`

These classifications are used to choose safer transition orderings.

### Transition Resolution

`resolve_transition()` takes a start pose, target pose, and duration. It returns one or more trajectory steps.

The resolver handles these cases:

| Case | Safer behavior |
|---|---|
| Returning to open palm | Uses thumb relation to decide whether to release fingers first or move thumb out first. |
| Under-to-over transition | Moves blocking fingers to clearance, moves thumb to a calibrated safe pose, then moves to the target. |
| Over-to-under transition | Moves thumb out, releases fingers, moves thumb toward target, then finishes the target pose. |
| Over-thumb pose to opening fingers | Moves thumb out first, moves fingers, then moves thumb to target. |
| Thumb and fingers moving together | Splits motion so thumb and fingers do not move together directly. |
| Thumb-only movement | Moves blocking fingers to clearance before moving the thumb when needed. |
| Finger-only movement | Allows the finger target directly. Letter-specific sequences are responsible for internal ordering. |

## Trajectory Safety

`make_trajectory_safe()` processes a raw trajectory step by step.

For each transition, it:

1. Sanitizes the raw trajectory.
2. Looks at the current safe pose.
3. Resolves the transition to the next target pose.
4. Adds any inserted clearance or release steps.
5. Returns the final safe trajectory.



## Current Limitations

- The calibration scripts depend on user observation and manual labeling.
- The pinky is not part of the thumb safety calibration data, although it is included in full poses.
- Thumb relation detection in `safety.py` is rule-based and based on calibrated patterns.


## Project Status

The project currently supports safe transition generation for AeroHand poses using calibration data, thumb clearance rules, and thumb/finger relationship handling. 
