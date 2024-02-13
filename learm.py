import xarm

"""
---------------------------------
Author: Torin Perkins
---------------------------------
This is a controller class that was created based on the xarm library to handle my needs of the arm
---------------------------------
"""


class LeArm:
    arm = xarm.Controller('USB', debug=False)

    # ID's
    CLAW_ID = 1
    WRIST_R_ID = 2
    WRIST_V_ID = 3
    ELBOW_ID = 4
    SHOULDER_V_ID = 5
    SHOULDER_R_ID = 6

    # Ranges and Positions
    SERVO_RANGE = [500, 2500]
    CLAW_OPEN = 1500
    CLAW_CLOSE = 2450

    # Servos
    claw = xarm.Servo(CLAW_ID)
    wrist_r = xarm.Servo(WRIST_R_ID)
    wrist_v = xarm.Servo(WRIST_V_ID)
    elbow = xarm.Servo(ELBOW_ID)
    shoulder_v = xarm.Servo(SHOULDER_V_ID)
    shoulder_r = xarm.Servo(SHOULDER_R_ID)

    # Init Positions
    claw_init_pos = 1500
    wrist_r_init_pos = 1500
    wrist_v_init_pos = 1500
    elbow_init_pos = 1500
    shoulder_v_init_pos = 1500
    shoulder_r_init_pos = 1500

    def __init__(self):
        # Initialize all servos
        self.openClaw(False)
        self.rotateWrist(self.wrist_r_init_pos, False)
        self.moveWrist_V(self.wrist_v_init_pos, False)
        self.moveElbow(self.elbow_init_pos, False)
        self.moveShoulder_V(self.shoulder_v_init_pos, False)
        self.rotateArm(self.shoulder_r_init_pos, False)

        print("Claw Init Pos:", self.claw_init_pos)
        print("Wrist R Init Pos:", self.wrist_r_init_pos)
        print("Wrist V Init Pos:", self.wrist_v_init_pos)
        print("Elbow Init Pos:", self.elbow_init_pos)
        print("Shoulder V Init Pos:", self.shoulder_v_init_pos)
        print("Shoulder R Init Pos:", self.shoulder_r_init_pos)


    def closeClaw(self, wait):
        """
        closes the gripper
        :param wait: should we wait on this being done?
        :return: None
        """
        self.arm.setPosition(self.CLAW_ID, self.CLAW_CLOSE, wait=wait)

    def openClaw(self, wait):
        """
        opens the gripper
        :param wait: should we wait on this being done?
        :return: None
        """
        self.arm.setPosition(self.CLAW_ID, self.CLAW_OPEN, wait=wait)

    def rotateWrist(self, position, wait):
        """
        rotates the wrist
        :param position: position of servo
        :param wait: should we wait on this being done?
        :return: None
        """
        if self.SERVO_RANGE[1] >= position >= self.SERVO_RANGE[0]:
            self.arm.setPosition(self.WRIST_R_ID, position, wait=wait)
        else:
            print("Out of Range")

    def moveWrist_V(self, position, wait):
        """
        moves the wrist vertically
        :param position: position of servo
        :param wait: should we wait on this being done?
        :return: None
        """
        if self.SERVO_RANGE[1] >= position >= self.SERVO_RANGE[0]:
            self.arm.setPosition(self.WRIST_V_ID, position, wait=wait)
        else:
            print("Out of Range")

    def moveElbow(self, position, wait):
        """
        moves the elbow
        :param position: position of the servo
        :param wait: should we wait on this being done?
        :return: None
        """
        if self.SERVO_RANGE[1] >= position >= self.SERVO_RANGE[0]:
            self.arm.setPosition(self.ELBOW_ID, position, wait=wait)
        else:
            print("Out of Range")

    def moveShoulder_V(self, position, wait):
        """
        moves the shoulder vertically
        :param position: position of the servo
        :param wait: should we wait on this being done?
        :return: None
        """
        if self.SERVO_RANGE[1] >= position >= self.SERVO_RANGE[0]:
            self.arm.setPosition(self.SHOULDER_V_ID, position, wait=wait)
        else:
            print("Out of Range")

    def rotateArm(self, position, wait):
        """
        rotates the arm
        :param position: position of the servo
        :param wait: should we wait on this being done?
        :return: None
        """
        if self.SERVO_RANGE[1] >= position >= self.SERVO_RANGE[0]:
            self.arm.setPosition(self.SHOULDER_R_ID, position, wait=wait)
        else:
            print("Out of Range")

    def moveToPosition(self, pos_array, wait=False):
        """
        moves whole arm to given position
        :param pos_array: array of positions
        :return: None
        """

        self.rotateWrist(pos_array[0], wait)
        self.moveWrist_V(pos_array[1], wait)
        self.moveElbow(pos_array[2], wait)
        self.moveShoulder_V(pos_array[3], wait)
        self.rotateArm(pos_array[4], wait)
