#!/usr/bin/env python3
"""Basic connection example.

Demonstrates how to connect to a Dobot robot using the unified
``DobotRobot.connect()`` factory method and inspect the resulting
object.  The factory automatically selects the correct protocol
(V3 or V4) based on the model string you provide.

Difficulty: Beginner
Prerequisites: pip install -e ".[dev]", robot powered on and reachable
"""

from ts_dobot_api import DobotRobot

# -- Configuration --------------------------------------------------------
# Change these values to match your setup.
ROBOT_IP = "192.168.5.1"
ROBOT_MODEL = "CR"  # One of: "CR", "NOVA", "NOVA_2S", "NOVA_NG"


def main() -> None:
    """Connect, print robot information, and disconnect."""
    # DobotRobot.connect() is the recommended entry point.
    # It returns either a DobotRobotV3 or DobotRobotV4 depending on the model.
    with DobotRobot.connect(ROBOT_IP, model=ROBOT_MODEL) as robot:
        print(f"Connected: {robot}")
        print(f"  IP:          {robot.ip}")
        print(f"  Model:       {robot.model}")
        print(f"  Family:      {robot.family.display_name}")
        print(f"  API version: {robot.api_version.value}")


if __name__ == "__main__":
    main()
