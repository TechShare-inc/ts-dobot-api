#!/usr/bin/env python3
"""Error handling example.

Demonstrates how to check for controller alarms, clear them, and
catch project-specific exceptions.  The wrapper exposes
``TsDobotError`` as the base class for all custom exceptions so you
can handle them in a single ``except`` clause.

Difficulty: Intermediate
Prerequisites: 03_reading_state.py completed successfully
"""

from ts_dobot_api import DobotRobot
from ts_dobot_api.exceptions import StartupError, TsDobotError

# -- Configuration --------------------------------------------------------
ROBOT_IP = "192.168.5.1"
ROBOT_MODEL = "NOVA"


def main() -> None:
    """Show alarm checking, clearing, and exception handling."""
    try:
        with DobotRobot.connect(ROBOT_IP, model=ROBOT_MODEL) as robot:
            # --- Check for active alarms ---------------------------------
            has_errors = robot.error_handling.check_errors()
            print(f"Has active alarms: {has_errors}")

            if has_errors:
                error_ids = robot.query.get_error_id()
                print(f"Active error IDs: {error_ids}")

                # Attempt to clear and recover automatically.
                recovered = robot.error_handling.clear_and_recover()
                print(f"Recovery result: {'success' if recovered else 'failed'}")

            # --- Normal operation ----------------------------------------
            robot.lifecycle.startup(speed=20)
            pose = robot.query.get_pose()
            print(f"Current pose: {pose.as_tuple()}")
            robot.lifecycle.shutdown()

    except StartupError as exc:
        # Raised when the startup sequence itself fails.
        print(f"Startup failed: {exc}")
    except TsDobotError as exc:
        # Catch-all for any wrapper-level error.
        print(f"Robot error: {exc}")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")


if __name__ == "__main__":
    main()
