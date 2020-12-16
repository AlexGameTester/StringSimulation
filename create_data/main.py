from math import *

import config


class DataCreate:
    def __init__(self):
        self.greeting_text = []
        with open('greeting.txt', 'r') as greeting_file:
            for string in greeting_file:
                self.greeting_text.append(string.strip())

        self.file_name = 'default_name'
        self.amount_of_points = None

        self.txt_generated = False
        self.is_active = True

    def greeting(self):
        for greeting_string in self.greeting_text:
            print(greeting_string)

    def generate_txt_file(self):
        self.get_filename()
        self.get_amount_of_points()
        while not self.txt_generated:
            print("Enter function for v_y(x) (for ex sin(x))\n----> ")
            function = input()
            try:
                self.create_init_params(function)
                self.txt_generated = True
            except Exception:
                self.txt_generated = False
                self.talk()
                self.generate_txt_file()

            self.talk()
            self.txt_generated = True

    def get_filename(self):
        print("\nEnter a name for the new file (without .txt): ")
        self.file_name = input()
        self.file_name += '.txt'
        print(f"OK. The future file name is {self.file_name}\n")

    def get_amount_of_points(self):
        print("Enter the number of points in the file: ")
        self.amount_of_points = int(input())
        print(f"Ok. The cord is modeled from {self.amount_of_points} points\n")

    def create_init_params(self, function):
        print(function)

        delta_r = config.SCREEN_WIDTH / (2*self.amount_of_points)
        x = 0
        y = 0
        max_velocity = 0.4
        with open(self.file_name, "w") as points:
            for i in range(self.amount_of_points):
                velocity = max_velocity * eval(function)
                point = str(x) + " " + str(y) + " " + str(velocity) + "\n"
                points.write(point)

                x += delta_r

    def talk(self):
        if self.txt_generated and self.is_active:
            print("Good. File created!\n")
            self.is_active = False
        elif not self.txt_generated and self.is_active:
            print("The file could not be created. Try again.\n")
        elif not self.txt_generated and not self.is_active:
            print("The program is turned off. File not created\n")


def main():
    data_create = DataCreate()
    data_create.greeting()
    data_create.generate_txt_file()


if __name__ == "__main__":
    main()
