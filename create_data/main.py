from math import *
import os

import config

MAX_POINTS = 10000


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
        try:
            self.get_amount_of_points()
        except Exception as err:
            print("!!ERROR!! --- ", err)

        while not self.txt_generated:
            print("Enter function for y(x)\n"
                  "For example sin(2*pi*x/450)\n----> ")
            function = input()
            try:
                self.create_init_params(function)
                self.txt_generated = True
            except Exception as err:
                print("!!ERROR!! --- ", err)
                self.txt_generated = False
                self.talk()
                self.generate_txt_file()

            self.talk()

    def get_filename(self):
        print("\nEnter a name for the new file (without .txt): ")
        self.file_name = input()
        self.file_name += '.txt'
        print(f"OK. The future file name is {self.file_name}\n")

    def get_amount_of_points(self):
        print("Enter the number of points in the file: ")
        self.amount_of_points = int(input())
        if self.amount_of_points <= 0:
            raise ValueError('Number of points must be positive')
        elif self.amount_of_points > MAX_POINTS:
            raise ValueError(f'Number of points must be at most {MAX_POINTS}')
        print(f"Ok. The cord is modeled from {self.amount_of_points} points\n")

    def create_init_params(self, function):
        os.chdir('../data')
        delta_r = config.SCREEN_WIDTH / (2*self.amount_of_points)
        max_y_coordinate = config.SCREEN_HEIGHT / 40
        y_coordinates = []

        x = point_number = 0
        while point_number < self.amount_of_points:
            y_coordinates.append(eval(function))
            x += delta_r
            point_number += 1

        y_abs = [abs(y) for y in y_coordinates]
        max_y = max(y_abs)
        for num, y in enumerate(y_coordinates):
            y_coordinates[num] = y * max_y_coordinate / max_y

        x = velocity = 0
        with open(self.file_name, "w") as points:
            for y in y_coordinates:
                record = str(x) + " " + str(y) + " " + str(velocity) + "\n"
                points.write(record)
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
