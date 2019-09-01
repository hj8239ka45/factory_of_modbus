import serial
import sys
import os
import time

class RoboticArm:
    def __init__(self, com_port):
        self.comport = com_port
        self.braudrate = 9600
        self.robotic_arm = serial.Serial(self.comport, self.braudrate, xonxoff=True, timeout=0.25)
        self.a = "492.085,0,393.72,0,0"
        self.b = "492.085,0,595.978,0,0"
        self.c = "204.042,0,595.978,0,0"
        self.d = "0,204.0419,595.978,0,0"
        self.e_1 = "0,600.497,595.978,0,0"
        self.e_2 = "0,626.854,595.978,0,0"
        self.e_3 = "0,569.276,595.978,0,0"
        self.f_1 = "0,600.497,393.72,0,0"
        self.f_2 = "0,626.854,219.806,0,0"
        self.f_3 = "0,569.276,290.119,0,0"
        self.g = "-204.0419,0,595.978,0,0"
        self.h = "-424.979,-48.219,595.978,0,0"
        self.i = "-424.979,-48.219,219.025,0,0"
        self.move = "5MA "
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

    def grip(self):
        self.robotic_arm.write("T5N0=2".encode() + os.linesep.encode())
        while True:
            message = self.robotic_arm.readline(50)
            print(message)
            if message.find("Ok".encode()) != -1:
                break
        time.sleep(1)
        # self.robotic_arm.write("WT 100".encode() + os.linesep.encode())

    def ungrip(self):
        self.robotic_arm.write("T5N0=3".encode() + os.linesep.encode())
        while True:
            message = self.robotic_arm.readline(50)
            print(message)
            if message.find("Ok".encode()) != -1:
                break
        time.sleep(1)
        # self.robotic_arm.write("WT 100".encode() + os.linesep.encode())

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

