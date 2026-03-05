#!/usr/bin/env python3
"""Configuration example.

Demonstrates how to configure motion parameters, coordinate systems,
payload, and collision detection on the robot.  The ``config`` namespace
controls maximum velocities, accelerations, and blending ratios that
apply to subsequent motion commands.  The ``system`` namespace provides
the global speed factor.

All parameters are set to conservative defaults so the robot moves
slowly and predictably — suitable for first-time experimentation.

Difficulty: Intermediate
Prerequisites: 04_error_handling.py completed successfully
"""

import time

from ts_dobot_api import DobotRobot

# -- Configuration --------------------------------------------------------
ROBOT_IP = "192.168.5.1"
ROBOT_MODEL = "NOVA"  # One of: "CR", "NOVA", "NOVA_2S", "NOVA_NG"

# Conservative motion defaults.
JOINT_VELOCITY = 20  # % of maximum joint speed
CARTESIAN_VELOCITY = 100  # mm/s
JOINT_ACCEL = 20  # % of maximum joint acceleration
CARTESIAN_ACCEL = 100  # mm/s²
CP_RATIO = 0  # continuous-path blending (0 = stop at each point)

# Path offset for a test move (mm).
_DX = 50.0


def main() -> None:
    """Configure motion parameters, execute a move, then restore defaults."""
    with DobotRobot.connect(ROBOT_IP, model=ROBOT_MODEL) as robot:
        robot.lifecycle.startup(speed=30)
        time.sleep(1)

        # --- Global speed factor -----------------------------------------
        # SpeedFactor scales *all* motion (1-100 %).  Useful as a master
        # dial during commissioning — keeps every move slow regardless of
        # per-command overrides.
        robot.system.speed_factor(50)
        print("Global speed factor set to 50 %")

        # --- Per-axis velocity and acceleration --------------------------
        robot.config.vel_j(JOINT_VELOCITY)
        robot.config.acc_j(JOINT_ACCEL)
        print(f"Joint velocity={JOINT_VELOCITY} %, acceleration={JOINT_ACCEL} %")

        robot.config.vel_l(CARTESIAN_VELOCITY)
        robot.config.acc_l(CARTESIAN_ACCEL)
        print(f"Cartesian velocity={CARTESIAN_VELOCITY} mm/s, acceleration={CARTESIAN_ACCEL} mm/s²")

        # Continuous-path blending ratio.
        robot.config.cp(CP_RATIO)
        print(f"CP blending ratio={CP_RATIO}")

        # --- Coordinate systems ------------------------------------------
        # Select user coordinate system 0 (base frame) and tool 0 (flange).
        robot.config.set_user(0)
        robot.config.set_tool(0)
        print("User=0, Tool=0 selected")

        # --- Payload -----------------------------------------------------
        # Always set the correct payload before moving.  Incorrect payload
        # causes inaccurate dynamics and may trigger collision alarms.
        robot.config.set_payload(weight=0.0)
        print("Payload set to 0.0 kg (no end-effector)")

        # --- Collision detection level -----------------------------------
        # Level 0-5; higher = more sensitive.  Set to 0 to disable.
        robot.config.set_collision_level(3)
        print("Collision detection level=3")

        # --- Verify with a short move ------------------------------------
        pose = robot.query.get_pose()
        x0, y0, z0, rx0, ry0, rz0 = pose

        robot.motion.mov_l(x0 + _DX, y0, z0, rx0, ry0, rz0)
        robot.motion.sync()
        print("Test move complete — configuration applied successfully.")

        robot.motion.mov_l(x0, y0, z0, rx0, ry0, rz0)
        robot.motion.sync()
        print("Returned to start position.")

        robot.lifecycle.shutdown()


if __name__ == "__main__":
    main()
