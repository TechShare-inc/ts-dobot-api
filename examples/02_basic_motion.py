#!/usr/bin/env python3
"""Basic motion example.

Demonstrates the standard lifecycle (startup → move → sync → shutdown)
using joint-space and linear moves.  Every motion command is followed
by ``sync()`` so the robot finishes one move before the next begins.

Difficulty: Beginner
Prerequisites: 01_basic_connection.py completed successfully
"""

from ts_dobot_api import DobotRobot

# -- Configuration --------------------------------------------------------
ROBOT_IP = "192.168.5.1"
ROBOT_MODEL = "CR"


def main() -> None:
    """Run startup, execute basic moves, then shut down."""
    with DobotRobot.connect(ROBOT_IP, model=ROBOT_MODEL) as robot:
        # 1. Startup — clears errors, enables the robot, sets speed.
        robot.startup(speed=30)
        print("Robot started.")

        # 2. Joint move (MovJ) — the robot plans a joint-space path
        #    to the given Cartesian target.
        robot.mov_j(350.0, 0.0, 200.0, 0.0, 0.0, 0.0)
        robot.sync()
        print("Joint move complete.")

        # 3. Linear move (MovL) — the robot moves in a straight line.
        robot.mov_l(350.0, 100.0, 200.0, 0.0, 0.0, 0.0)
        robot.sync()
        print("Linear move complete.")

        # 4. Move back to the start position.
        robot.mov_j(350.0, 0.0, 200.0, 0.0, 0.0, 0.0)
        robot.sync()
        print("Returned to start position.")

        # 5. Shutdown — disables the robot arm gracefully.
        robot.shutdown()
        print("Robot shut down.")


if __name__ == "__main__":
    main()
