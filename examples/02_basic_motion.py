#!/usr/bin/env python3
"""Basic motion example.

Demonstrates the standard lifecycle (startup → read state → move → sync →
shutdown) using joint-space moves, linear moves, and a circular arc move.
All motion targets are calculated from the robot's current state so the
example works from any starting position.  Every motion command is followed
by ``sync()`` so the robot finishes one move before the next begins.

Difficulty: Beginner
Prerequisites: 01_basic_connection.py completed successfully
"""

from ts_dobot_api import DobotRobot

# -- Configuration --------------------------------------------------------
ROBOT_IP = "192.168.5.1"
ROBOT_MODEL = "CR"

# Path offsets (mm) applied to the start pose to build waypoints.
_DX = 100.0  # step in X for the joint move
_DY = 100.0  # step in Y for the linear move; also sets circle radius


def main() -> None:
    """Run startup, read state, execute basic moves, then shut down."""
    with DobotRobot.connect(ROBOT_IP, model=ROBOT_MODEL) as robot:
        # 1. Startup — clears errors, enables the robot, sets speed.
        robot.startup(speed=30)
        print("Robot started.")

        # 2. Read current state so every target is relative to wherever
        #    the robot happens to be after startup.
        joints = robot.get_angle()  # j1-j6 in degrees (returned as Pose)
        pose = robot.get_pose()  # Cartesian: x, y, z, rx, ry, rz (mm / °)
        print(f"Joint angles : {joints}")
        print(f"Cartesian    : {pose}")

        x0, y0, z0, rx0, ry0, rz0 = pose  # unpack start position

        # 3a. Joint move (MovJ) — the robot plans a joint-space path
        #     to the target; orientation is unchanged.
        robot.mov_j(x0 + _DX, y0, z0, rx0, ry0, rz0)
        robot.sync()
        print("Joint move complete.")

        # 3b. Linear move (MovL) — the TCP travels in a straight line.
        robot.mov_l(x0 + _DX, y0 + _DY, z0, rx0, ry0, rz0)
        robot.sync()
        print("Linear move complete.")

        # 3c. Circular move — one full circle defined by the current position
        #     plus two via-points.  The three points must not be collinear.
        #     After one revolution the TCP returns to the starting point of
        #     this segment automatically.
        #
        #     via-point 1: opposite side of the circle
        #     via-point 2: three-quarter point
        #
        #     Note: ``circle()`` is V4-only; on V3 use ``arc()`` instead.
        robot.circle(
            x0,
            y0 + _DY,
            z0,
            rx0,
            ry0,
            rz0,  # via-point 1
            x0 + _DX,
            y0,
            z0,
            rx0,
            ry0,
            rz0,  # via-point 2
        )
        robot.sync()
        print("Circular move complete.")

        # 4. Shutdown — disables the robot arm gracefully.
        robot.shutdown()
        print("Robot shut down.")


if __name__ == "__main__":
    main()
