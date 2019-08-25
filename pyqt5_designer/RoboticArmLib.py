import serial
import os


class RoboticArm:
    def __init__(self, com_port):
        self.comport = com_port
        self.braudrate = 9600
        self.robotic_arm = serial.Serial(self.comport, self.braudrate, xonxoff=True, timeout=0.25)
        self.move_to_workpiece_table_instructions = ("5MA",
                                                     "5MA",
                                                     "5MA")
        self.back_from_workpiece_table_instructions = ("5MA",
                                                       "5MA",
                                                       "5MA")
        self.move_to_machine1_instructions = ("5MA",
                                              "5MA",
                                              "5MA")
        self.back_from_machine1_instructions = ("5MA",
                                                "5MA",
                                                "5MA")
        self.move_to_machine2_instructions = ("5MA",
                                              "5MA",
                                              "5MA")
        self.back_from_machine2_instructions = ("5MA",
                                                "5MA",
                                                "5MA")
        self.move_to_machine3_instructions = ("5MA",
                                              "5MA",
                                              "5MA")
        self.back_from_machine3_instructions = ("5MA",
                                                "5MA",
                                                "5MA")
        self.move_to_machine4_instructions = ("5MA",
                                              "5MA",
                                              "5MA",
                                              "5MA")
        self.back_from_machine4_instructions = ("5MA",
                                                "5MA",
                                                "5MA",
                                                "5MA")

    def grip(self):
        self.robotic_arm.write("T5N0=3".encode() + os.linesep.encode())

    def ungrip(self):
        self.robotic_arm.write("T5N0=2".encode() + os.linesep.encode())

    #
    # All move_to_XXX_XXX is from origin of initial coordinate
    # All back_from_XXX_XXX is back to origin of initial coordinate
    #
    def move_to_workpiece_table(self):
        for instruction in self.move_to_workpiece_table_instructions:
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())
            while True:
                message = self.robotic_arm.readline(50)
                print(message)
                if message.find("Sync done".encode()) != -1:
                    break

    def back_from_workpiece_table(self):
        for instruction in self.back_from_workpiece_table_instructions:
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())
            while True:
                message = self.robotic_arm.readline(50)
                print(message)
                if message.find("Sync done".encode()) != -1:
                    break

    def move_to_machine1(self):
        for instruction in self.move_to_machine1_instructions:
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())
            while True:
                message = self.robotic_arm.readline(50)
                print(message)
                if message.find("Sync done".encode()) != -1:
                    break

    def back_from_machine1(self):
        for instruction in self.back_from_machine1_instructions:
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())
            while True:
                message = self.robotic_arm.readline(50)
                print(message)
                if message.find("Sync done".encode()) != -1:
                    break

    def move_to_machine2(self):
        for instruction in self.move_to_machine2_instructions:
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())
            while True:
                message = self.robotic_arm.readline(50)
                print(message)
                if message.find("Sync done".encode()) != -1:
                    break

    def back_from_machine2(self):
        for instruction in self.back_from_machine2_instructions:
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())
            while True:
                message = self.robotic_arm.readline(50)
                print(message)
                if message.find("Sync done".encode()) != -1:
                    break

    def move_to_machine3(self):
        for instruction in self.move_to_machine3_instructions:
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())
            while True:
                message = self.robotic_arm.readline(50)
                print(message)
                if message.find("Sync done".encode()) != -1:
                    break

    def back_from_machine3(self):
        for instruction in self.back_from_machine3_instructions:
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())
            while True:
                message = self.robotic_arm.readline(50)
                print(message)
                if message.find("Sync done".encode()) != -1:
                    break

    def move_to_machine4(self):
        for instruction in self.move_to_machine4_instructions:
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())
            while True:
                message = self.robotic_arm.readline(50)
                print(message)
                if message.find("Sync done".encode()) != -1:
                    break

    def back_from_machine4(self):
        for instruction in self.back_from_machine4_instructions:
            self.robotic_arm.write(instruction.encode() + os.linesep.encode())
            while True:
                message = self.robotic_arm.readline(50)
                print(message)
                if message.find("Sync done".encode()) != -1:
                    break

