#!/usr/bin/env python3
"""Feedback data example.

Demonstrates how to read real-time feedback from the robot controller.
The ``feedback_data()`` method returns a ``FeedbackData`` dataclass with
fields such as current joint positions, velocities, and torques.

Difficulty: Intermediate
Prerequisites: 05_io_control.py completed successfully
"""

import time

from ts_dobot_api import DobotRobot

# -- Configuration --------------------------------------------------------
ROBOT_IP = "192.168.5.1"
ROBOT_MODEL = "NOVA"

# How many samples to read.
SAMPLE_COUNT = 5
SAMPLE_INTERVAL = 0.5  # seconds


def main() -> None:
    """Read and display real-time feedback samples."""
    with DobotRobot.connect(ROBOT_IP, model=ROBOT_MODEL) as robot:
        robot.lifecycle.startup(speed=20)

        print(
            f"Reading {SAMPLE_COUNT} feedback samples (interval={SAMPLE_INTERVAL}s):\n"
        )

        try:
            for i in range(SAMPLE_COUNT):
                data = robot.feedback.feedback_data()
                if data is None:
                    print(f"  [{i + 1}] No feedback data received.")
                    continue

                # FeedbackData is a rich dataclass — print a summary.
                print(f"  [{i + 1}] {data}")
                time.sleep(SAMPLE_INTERVAL)
        except KeyboardInterrupt:
            print("\nSampling interrupted by user.")

        robot.lifecycle.shutdown()


if __name__ == "__main__":
    main()
