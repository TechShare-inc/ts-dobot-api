#!/usr/bin/env python3
"""Reading state example.

Shows how to query the robot's current Cartesian pose, joint angles,
and operating mode after startup.  The returned ``Pose`` is a frozen
dataclass that can be unpacked as a tuple for convenience.

Also demonstrates V4-only kinematics: ``positive_kin()`` (joint angles
→ Cartesian) and ``inverse_kin()`` (Cartesian → joint angles).

Difficulty: Beginner
Prerequisites: 02_basic_motion.py completed successfully
"""

from ts_dobot_api import DobotRobot

# -- Configuration --------------------------------------------------------
ROBOT_IP = "192.168.5.1"
ROBOT_MODEL = "NOVA"


def main() -> None:
    """Query and display the robot's current state."""
    with DobotRobot.connect(ROBOT_IP, model=ROBOT_MODEL) as robot:
        robot.lifecycle.startup(speed=30)

        # Current Cartesian pose (x, y, z, rx, ry, rz).
        pose = robot.query.get_pose()
        print(f"Cartesian pose: x={pose.x:.2f}, y={pose.y:.2f}, z={pose.z:.2f}")
        print(f"                rx={pose.rx:.2f}, ry={pose.ry:.2f}, rz={pose.rz:.2f}")

        # Pose can be unpacked as a tuple.
        coords = pose.as_tuple()
        print(f"As tuple: {coords}")

        # Current joint angles (j1-j6 mapped into the same Pose fields).
        angles = robot.query.get_angle()
        print(f"Joint angles: {angles.as_tuple()}")

        # Robot operating mode (integer code).
        mode = robot.query.robot_mode()
        print(f"Robot mode: {mode}")

        # --- V4-only: kinematics -----------------------------------------
        # positive_kin: compute the Cartesian pose for a given set of
        # joint angles without actually moving the robot.
        # Raises NotImplementedError on V3.
        try:
            fk = robot.query.positive_kin(
                angles.x,
                angles.y,
                angles.z,
                angles.rx,
                angles.ry,
                angles.rz,
            )
            print(f"FK (positive_kin): x={fk.x:.2f}, y={fk.y:.2f}, z={fk.z:.2f}")

            # inverse_kin: compute joint angles for a given Cartesian pose.
            ik = robot.query.inverse_kin(
                pose.x,
                pose.y,
                pose.z,
                pose.rx,
                pose.ry,
                pose.rz,
            )
            print(f"IK (inverse_kin): j1={ik.x:.2f}, j2={ik.y:.2f}, j3={ik.z:.2f}")

            # get_current_command_id: poll the motion-queue position.
            cmd_id = robot.query.get_current_command_id()
            print(f"Current command ID: {cmd_id}")
        except NotImplementedError:
            print("Kinematics queries not available on this robot (V3).")

        robot.lifecycle.shutdown()


if __name__ == "__main__":
    main()
