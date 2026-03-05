#!/usr/bin/env python3
"""V4-only and native SDK access example.

Demonstrates two tiers of V4-exclusive functionality:

1. **V4-only methods on the unified wrapper** — these raise
   ``NotImplementedError`` on V3 but call directly on ``robot``:
   force-sensor control, kinematics, full-circle motion, trajectory
   playback, and script control.

2. **Advanced native-only access** — features too specialised for
   the unified wrapper (modbus, conveyor tracking, motion pre-checks,
   advanced force compliance).  These require the ``.native.dashboard``
   escape hatch.

Difficulty: Advanced
Prerequisites: 06_feedback_data.py completed successfully
"""

import time

from ts_dobot_api import DobotRobot

# -- Configuration --------------------------------------------------------
ROBOT_IP = "192.168.5.1"
ROBOT_MODEL = "CR"  # Must be a V4-family model for force-sensor features.


def demo_v4_wrapper_methods(robot: DobotRobot) -> None:  # type: ignore[type-arg]
    """Show V4-only methods available directly on the unified wrapper."""
    print("\n--- V4 unified wrapper methods ---")

    # Script/queue control.
    # robot.run_script("my_project")   # run a project on the controller
    # robot.pause_script()             # pause the motion queue
    # robot.resume_script()            # resume it
    # robot.stop_script()              # stop entirely

    # Forward kinematics: joint angles -> Cartesian pose.
    angles = robot.query.get_angle()
    fk_pose = robot.positive_kin(
        angles.x, angles.y, angles.z, angles.rx, angles.ry, angles.rz
    )
    print(f"FK result: x={fk_pose.x:.2f}, y={fk_pose.y:.2f}, z={fk_pose.z:.2f}")

    # Inverse kinematics: Cartesian pose -> joint angles.
    pose = robot.query.get_pose()
    ik_joints = robot.inverse_kin(pose.x, pose.y, pose.z, pose.rx, pose.ry, pose.rz)
    print(
        f"IK result: j1={ik_joints.x:.2f}, j2={ik_joints.y:.2f}, j3={ik_joints.z:.2f}"
    )

    # Poll the motion-queue command ID (useful for custom sync logic).
    cmd_id = robot.get_current_command_id()
    print(f"Current command ID: {cmd_id}")

    # Full-circle move: supply two via-points; `count` = number of laps.
    # robot.motion.circle(350, 0, 200, 0, 0, 0,  350, 50, 250, 0, 0, 0,  count=1)
    # robot.motion.sync()

    # Trajectory playback (file must exist on the controller).
    # start = robot.get_start_pose("my_trace")
    # print(f"Trajectory start pose: {start}")
    # robot.start_path("my_trace")
    # robot.motion.sync()

    # Force/torque sensor.
    print("\nForce sensor:")
    robot.force_control.enable_ft_sensor(1)  # enable sensor
    robot.six_force_home()  # zero the sensor
    time.sleep(0.2)
    force = robot.force_control.get_force()  # Fx, Fy, Fz, Tx, Ty, Tz
    print(
        f"  Fx={force.x:.2f} N  Fy={force.y:.2f} N  Fz={force.z:.2f} N"
        f"  Tx={force.rx:.2f} Nm  Ty={force.ry:.2f} Nm  Tz={force.rz:.2f} Nm"
    )
    robot.force_control.fc_off()  # turn off force-compliance mode
    robot.force_control.enable_ft_sensor(0)  # disable sensor


def demo_native_advanced(robot: DobotRobot) -> None:  # type: ignore[type-arg]
    """Show features that are only accessible via .native.dashboard."""
    print("\n--- Advanced native-only features ---")

    db = robot.native.dashboard  # type: ignore[union-attr]

    # Raw TCP command (lowest-level access).
    raw = robot.raw.send_raw("GetAngle()")
    print(f"Raw GetAngle() response: {raw}")

    # Motion pre-checks: validate a move before executing it.
    # Returns immediately with a pass/fail and collision info.
    # db.check_mov_j(j1a, j2a, j3a, j4a, j5a, j6a,
    #                j1b, j2b, j3b, j4b, j5b, j6b)
    # db.check_mov_l(...)  # same but for linear moves
    # db.check_mov_c(...)  # circular pre-check

    # Modbus: create a TCP master, read/write registers.
    # index = db.modbus_create("192.168.1.50", 502, slave_id=1)
    # val   = db.get_hold_regs(index, addr=0, count=4)
    # db.set_hold_regs(index, addr=0, count=1, val_tab="{100}", val_type="U16")
    # db.modbus_close(index)

    # Conveyor tracking.
    # db.cnv_init(1)           # initialise conveyor 1
    # db.start_sync_cnv()      # start synchronous tracking
    # db.cnv_mov_l(...)        # move alongside the conveyor
    # db.stop_sync_cnv()       # stop tracking

    # Welding / weave.
    # db.weave_start()
    # db.weave_params(weld_type=1, frequency=3.0,
    #                 left_amplitude=2.0, right_amplitude=2.0,
    #                 direction=0, stop_mode=0,
    #                 stop_time1=0, stop_time2=0,
    #                 stop_time3=0, stop_time4=0,
    #                 radius=0.0, radian=0.0)
    # db.weave_end()

    # Advanced force compliance (parameter-level control).
    # db.fc_force_mode(x=0, y=0, z=1, rx=0, ry=0, rz=0,   # free axes
    #                  fx=0, fy=0, fz=5, frx=0, fry=0, frz=0)  # target force
    # db.fc_set_stiffness(x=0, y=0, z=500, rx=0, ry=0, rz=0)
    # db.fc_set_damping(x=0, y=0, z=50, rx=0, ry=0, rz=0)
    # db.fc_set_force(x=0, y=0, z=5, rx=0, ry=0, rz=0)
    # robot.force_control.fc_off()   # turn off via wrapper

    print("(Advanced native-only calls shown as comments above.)")
    _ = db  # suppress unused-variable warning


def main() -> None:
    """Run V4-only wrapper demos and native-access demos."""
    with DobotRobot.connect(ROBOT_IP, model=ROBOT_MODEL) as robot:
        print(f"Connected: {robot}")
        robot.lifecycle.startup(speed=20)

        demo_v4_wrapper_methods(robot)
        demo_native_advanced(robot)

        robot.lifecycle.shutdown()


if __name__ == "__main__":
    main()
