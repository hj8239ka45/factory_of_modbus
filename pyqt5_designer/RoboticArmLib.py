import serial
import sys
import os
import time


class RoboticArm:
    def __init__(self, com_port):
        self.comport = com_port
        self.braudrate = 9600

        # Initialize connection with robotic arm
        self.robotic_arm = serial.Serial(self.comport, self.braudrate, xonxoff=True, timeout=1.5)

        # Set speed and acceleration of robotic arm
        self.spd = 100
        self.acl = 200

        # Set position of every point in process
        # For every machine
        self.a = "492.085,0,393.72,0,0"
        self.b = "492.085,0,595.978,0,0"
        self.c = "204.042,0,595.978,0,0"
        self.d = "0,204.0419,595.978,0,0"
        # For machine 1, machine 2, and machine 3
        self.e_1 = "0,600.497,410.978,0,0"
        self.e_2 = "0,626.854,400.978,0,0"
        self.e_3 = "0,569.276,400.978,0,0"
        self.f_1 = "0,600.497,383.72,0,0"
        self.f_2 = "0,626.854,219.806,0,0"
        self.f_3 = "0,569.276,290.119,0,0"
        self.g = "-204.0419,0,595.978,0,0"
        # Only for machine 4
        self.h = "-424.979,-48.219,595.978,0,0"
        self.i = "-424.979,-48.219,219.025,0,0"

        # Set behavior category of robotic arm
        self.move = "5MA "

        # Set complete instructions of every behavior of robotic arm
        self.move_to_workpiece_table_instructions = (self.move + self.b,
                                                     self.move + self.a)
        self.back_from_workpiece_table_instructions = (self.move + self.b,
                                                       self.move + self.c)
        self.move_to_machine1_instructions = (self.move + self.d,
                                              self.move + self.e_1,
                                              self.move + self.f_1)
        self.back_from_machine1_instructions = (self.move + self.e_1,
                                                self.move + self.d,
                                                self.move + self.c)
        self.move_to_machine2_instructions = (self.move + self.d,
                                              self.move + self.e_2,
                                              self.move + self.f_2)
        self.back_from_machine2_instructions = (self.move + self.e_2,
                                                self.move + self.d,
                                                self.move + self.c)
        self.move_to_machine3_instructions = (self.move + self.d,
                                              self.move + self.e_3,
                                              self.move + self.f_3)
        self.back_from_machine3_instructions = (self.move + self.e_3,
                                                self.move + self.d,
                                                self.move + self.c)
        self.move_to_machine4_instructions = (self.move + self.d,
                                              self.move + self.g,
                                              self.move + self.h,
                                              self.move + self.i)
        self.back_from_machine4_instructions = (self.move + self.h,
                                                self.move + self.g,
                                                self.move + self.d,
                                                self.move + self.c)
    def close(self):
        self.robotic_arm.close()
    # High, middle, and low speed and acceleration are (200, 400), (100, 200), and (50, 100) respectively
    def speed(self, spd=100, acl=200):
        # Make sure change accords with regulation
        if (spd == 200 and acl == 400) or (spd == 100 and acl == 200) or (spd == 50 and acl == 100):
            # Change value of speed and acceleration
            self.spd = spd
            self.acl = acl

            # Transfer value of acceleration to robotic arm
            self.robotic_arm.write("PR2=".encode() + str(self.acl).encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Ok")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Ok"
                if message.find("Ok".encode()) != -1:
                    # Break out loop and stop reading
                    break

            # Transfer value of speed to robotic arm
            self.robotic_arm.write("PR3=".encode() + str(self.spd).encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Ok")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Ok"
                if message.find("Ok".encode()) != -1:
                    # Break out loop and stop reading
                    break
        else:
            print("Please refer to regulation")

    def grip(self):
        # Transfer grip instruction
        self.robotic_arm.write("T5N0=2".encode() + os.linesep.encode())

        # Wait robotic arm transfers back message("ok")
        while True:
            # Read message of robotic arm
            message = self.robotic_arm.readline(50)
            print(message)
            # Make sure whether the message is "ok"
            if message.find("Ok".encode()) != -1:
                # Break out loop and stop reading
                break

        # Wait a second instead of "WT 100" because of no this instruction
        time.sleep(1)
        # self.robotic_arm.write("WT 100".encode() + os.linesep.encode())

    def ungrip(self):
        # Transfer ungrip instruction
        self.robotic_arm.write("T5N0=1".encode() + os.linesep.encode())

        # Wait robotic arm transfers back message("ok")
        while True:
            # Read message of robotic arm
            message = self.robotic_arm.readline(50)
            print(message)
            # Make sure whether the message is "ok"
            if message.find("Ok".encode()) != -1:
                # Break out loop and stop reading
                break

        # Wait a second instead of "WT 100" because of no this instruction
        time.sleep(1)
        # self.robotic_arm.write("WT 100".encode() + os.linesep.encode())

    #
    # All move_to_XXX is from origin of initial coordinate
    # All back_from_XXX is back to origin of initial coordinate
    #
    def move_to_workpiece_table(self):
        # Transfer all instructions one by one
        for instruction in self.move_to_workpiece_table_instructions:
            # Transfer one of all instructions
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Sync done")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Sync done"
                if message.find("Sync done".encode()) != -1:
                    # Break out loop and stop reading
                    break

    def back_from_workpiece_table(self):
        # Transfer all instructions one by one
        for instruction in self.back_from_workpiece_table_instructions:
            # Transfer one of all instructions
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Sync done")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Sync done"
                if message.find("Sync done".encode()) != -1:
                    # Break out loop and stop reading
                    break

    def move_to_machine1(self):
        # Transfer all instructions one by one
        for instruction in self.move_to_machine1_instructions:
            # Transfer one of all instructions
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Sync done")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Sync done"
                if message.find("Sync done".encode()) != -1:
                    # Break out loop and stop reading
                    break

    def back_from_machine1(self):
        # Transfer all instructions one by one
        for instruction in self.back_from_machine1_instructions:
            # Transfer one of all instructions
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Sync done")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Sync done"
                if message.find("Sync done".encode()) != -1:
                    # Break out loop and stop reading
                    break

    def move_to_machine2(self):
        # Transfer all instructions one by one
        for instruction in self.move_to_machine2_instructions:
            # Transfer one of all instructions
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Sync done")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Sync done"
                if message.find("Sync done".encode()) != -1:
                    # Break out loop and stop reading
                    break

    def back_from_machine2(self):
        # Transfer all instructions one by one
        for instruction in self.back_from_machine2_instructions:
            # Transfer one of all instructions
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Sync done")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Sync done"
                if message.find("Sync done".encode()) != -1:
                    # Break out loop and stop reading
                    break

    def move_to_machine3(self):
        # Transfer all instructions one by one
        for instruction in self.move_to_machine3_instructions:
            # Transfer one of all instructions
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Sync done")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Sync done"
                if message.find("Sync done".encode()) != -1:
                    # Break out loop and stop reading
                    break

    def back_from_machine3(self):
        # Transfer all instructions one by one
        for instruction in self.back_from_machine3_instructions:
            # Transfer one of all instructions
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Sync done")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Sync done"
                if message.find("Sync done".encode()) != -1:
                    # Break out loop and stop reading
                    break

    def move_to_machine4(self):
        # Transfer all instructions one by one
        for instruction in self.move_to_machine4_instructions:
            # Transfer one of all instructions
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Sync done")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Sync done"
                if message.find("Sync done".encode()) != -1:
                    # Break out loop and stop reading
                    break

    def back_from_machine4(self):
        # Transfer all instructions one by one
        for instruction in self.back_from_machine4_instructions:
            # Transfer one of all instructions
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())

            # Wait robotic arm transfers back message("Sync done")
            while True:
                # Read message of robotic arm
                message = self.robotic_arm.readline(50)
                print(message)
                # Make sure whether the message is "Sync done"
                if message.find("Sync done".encode()) != -1:
                    # Break out loop and stop reading
                    break

# =============================================================================
# # # # # # # Example # # # # # # #
# if __name__ == "__main__":
#     Jimmy = RoboticArm("COM8")
#
#     Jimmy.speed(200, 400)
#
#     Jimmy.move_to_workpiece_table()
#
#     Jimmy.grip()
#
#     Jimmy.back_from_workpiece_table()
#
#     Jimmy.speed(100, 200)
#
#     Jimmy.move_to_machine2()
#
#     Jimmy.ungrip()
#
#     Jimmy.back_from_machine2()
# =============================================================================