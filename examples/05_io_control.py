#!/usr/bin/env python3
"""I/O control example.

Demonstrates how to read and write digital and analogue I/O on the
robot controller.  This is commonly used to communicate with grippers,
sensors, and external PLCs.

Also covers V4-only extensions: setting outputs *immediately* (bypassing
the motion queue), reading output state back, and reading analogue inputs.

Difficulty: Intermediate
Prerequisites: 04_error_handling.py completed successfully
"""

import time

from ts_dobot_api import DobotRobot

# -- Configuration --------------------------------------------------------
ROBOT_IP = "192.168.5.1"
ROBOT_MODEL = "CR"

# Digital output indices (check your wiring diagram).
DO_INDEX = 1
TOOL_DO_INDEX = 1

# Analogue output index.
AO_INDEX = 1


def main() -> None:
    """Read and write digital/analogue I/O."""
    with DobotRobot.connect(ROBOT_IP, model=ROBOT_MODEL) as robot:
        robot.startup(speed=20)

        # --- Digital outputs (queued) ------------------------------------
        # These commands are inserted into the motion queue and execute
        # in order with any pending move commands.
        robot.do_output(DO_INDEX, status=1)
        print(f"DO{DO_INDEX} set to ON")
        time.sleep(0.5)

        robot.do_output(DO_INDEX, status=0)
        print(f"DO{DO_INDEX} set to OFF")

        # Tool digital output.
        robot.tool_do(TOOL_DO_INDEX, status=1)
        print(f"Tool DO{TOOL_DO_INDEX} set to ON")
        time.sleep(0.5)

        robot.tool_do(TOOL_DO_INDEX, status=0)
        print(f"Tool DO{TOOL_DO_INDEX} set to OFF")

        # --- Digital inputs ----------------------------------------------
        di_value = robot.di(DO_INDEX)
        print(f"DI{DO_INDEX} = {di_value}")

        tool_di_value = robot.tool_di(TOOL_DO_INDEX)
        print(f"Tool DI{TOOL_DO_INDEX} = {tool_di_value}")

        # --- Analogue output ---------------------------------------------
        robot.ao(AO_INDEX, value=2.5)
        print(f"AO{AO_INDEX} set to 2.5 V")
        time.sleep(0.5)

        robot.ao(AO_INDEX, value=0.0)
        print(f"AO{AO_INDEX} set to 0.0 V")

        # --- V4-only: immediate I/O (not queued) -------------------------
        # do_instant / tool_do_instant / ao_instant take effect right now,
        # independent of the motion queue.  Useful for time-critical
        # signals between motion commands.
        # Raises NotImplementedError on V3.
        try:
            robot.do_instant(DO_INDEX, status=1)
            print(f"DO{DO_INDEX} set immediately to ON (not queued)")
            time.sleep(0.2)
            robot.do_instant(DO_INDEX, status=0)

            robot.tool_do_instant(TOOL_DO_INDEX, status=1)
            print(f"Tool DO{TOOL_DO_INDEX} set immediately to ON")
            time.sleep(0.2)
            robot.tool_do_instant(TOOL_DO_INDEX, status=0)

            robot.ao_instant(AO_INDEX, value=1.5)
            print(f"AO{AO_INDEX} set immediately to 1.5 V")
            time.sleep(0.2)
            robot.ao_instant(AO_INDEX, value=0.0)
        except NotImplementedError:
            print("Instant I/O not available on this robot (V3).")

        # --- V4-only: read output and input state back -------------------
        try:
            do_state = robot.get_do(DO_INDEX)
            print(f"Current DO{DO_INDEX} state: {do_state}")

            tool_do_state = robot.get_tool_do(TOOL_DO_INDEX)
            print(f"Current Tool DO{TOOL_DO_INDEX} state: {tool_do_state}")

            ao_value = robot.get_ao(AO_INDEX)
            print(f"Current AO{AO_INDEX} value: {ao_value:.3f} V")

            ai_value = robot.ai(AO_INDEX)
            print(f"AI{AO_INDEX} = {ai_value}")

            tool_ai_value = robot.tool_ai(1)
            print(f"Tool AI1 = {tool_ai_value}")
        except NotImplementedError:
            print("Output/input reads not available on this robot (V3).")

        robot.shutdown()


if __name__ == "__main__":
    main()
