#!/usr/bin/env python3
"""Relative motion example.

Demonstrates how to move the robot by *offsets* rather than absolute
targets.  The ``relative_motion`` namespace provides moves in both the
tool coordinate frame and the user (world) coordinate frame.

Relative moves are especially useful when you need to shift the TCP by
a known distance from wherever it happens to be — for example, approach
a surface, retract after pick/place, or trace a pattern around the
current position.

Difficulty: Intermediate
Prerequisites: 08_configuration.py completed successfully
"""

import time

from ts_dobot_api import DobotRobot

# -- Configuration --------------------------------------------------------
ROBOT_IP = "192.168.5.1"
ROBOT_MODEL = "NOVA_NG"  # One of: "CR", "NOVA", "NOVA_2S", "NOVA_NG"

# Small offsets (mm / °) to keep moves safe.
OFFSET_Z = 30.0  # move 30 mm along Z
OFFSET_X = 50.0  # move 50 mm along X


def main() -> None:
    """Execute relative moves in tool-frame and user-frame coordinates."""
    with DobotRobot.connect(ROBOT_IP, model=ROBOT_MODEL) as robot:
        robot.lifecycle.startup(speed=20)
        time.sleep(1)

        start_pose = robot.query.get_pose()
        print(f"Start pose: {start_pose.as_tuple()}")

        # --- Relative linear move in TOOL frame -------------------------
        # Moves the TCP along the tool Z-axis (approach direction).
        # Only the offset axes move; all others stay at zero.
        print("\n-- Relative moves in tool frame --")

        robot.relative_motion.rel_mov_l_tool(0.0, 0.0, OFFSET_Z, 0.0, 0.0, 0.0)
        robot.motion.sync()
        print(f"  Moved +{OFFSET_Z} mm along tool Z")

        robot.relative_motion.rel_mov_l_tool(0.0, 0.0, -OFFSET_Z, 0.0, 0.0, 0.0)
        robot.motion.sync()
        print(f"  Returned -{OFFSET_Z} mm along tool Z")

        # --- Relative joint move in TOOL frame ---------------------------
        # Same offset but the planner uses joint interpolation instead of
        # a straight Cartesian line — faster for large moves.
        robot.relative_motion.rel_mov_j_tool(OFFSET_X, 0.0, 0.0, 0.0, 0.0, 0.0)
        robot.motion.sync()
        print(f"  Joint-move +{OFFSET_X} mm along tool X")

        robot.relative_motion.rel_mov_j_tool(-OFFSET_X, 0.0, 0.0, 0.0, 0.0, 0.0)
        robot.motion.sync()
        print(f"  Returned -{OFFSET_X} mm along tool X")

        # --- Relative linear move in USER frame --------------------------
        # Offsets are applied in the active user coordinate system
        # (typically the world/base frame when user=0).
        print("\n-- Relative moves in user frame --")

        robot.relative_motion.rel_mov_l_user(0.0, 0.0, OFFSET_Z, 0.0, 0.0, 0.0)
        robot.motion.sync()
        print(f"  Moved +{OFFSET_Z} mm along user Z (world up)")

        robot.relative_motion.rel_mov_l_user(0.0, 0.0, -OFFSET_Z, 0.0, 0.0, 0.0)
        robot.motion.sync()
        print(f"  Returned -{OFFSET_Z} mm along user Z")

        # --- Relative joint move in USER frame ---------------------------
        robot.relative_motion.rel_mov_j_user(OFFSET_X, 0.0, 0.0, 0.0, 0.0, 0.0)
        robot.motion.sync()
        print(f"  Joint-move +{OFFSET_X} mm along user X")

        robot.relative_motion.rel_mov_j_user(-OFFSET_X, 0.0, 0.0, 0.0, 0.0, 0.0)
        robot.motion.sync()
        print(f"  Returned -{OFFSET_X} mm along user X")

        # --- Relative joint-angle offset ---------------------------------
        # Shift individual joints by a small angle (degrees).
        print("\n-- Relative joint-angle offset --")

        robot.relative_motion.rel_joint_mov_j(5.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        robot.motion.sync()
        print("  J1 offset +5°")

        robot.relative_motion.rel_joint_mov_j(-5.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        robot.motion.sync()
        print("  J1 offset -5° (returned)")

        end_pose = robot.query.get_pose()
        print(f"\nEnd pose:   {end_pose.as_tuple()}")

        robot.lifecycle.shutdown()


if __name__ == "__main__":
    main()
