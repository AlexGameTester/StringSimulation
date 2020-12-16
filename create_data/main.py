from math import *

class DataCreate:
    def __init__(self):
        self.greeting_text = []
        with open('greeting.txt', 'r') as greeting_file:
            for string in greeting_file:
                self.greeting_text.append(string.strip())
        self.file_name = 'default_name'
        self.txt_generated = False
        self.is_active = True

    def greeting(self):
        for greeting_string in self.greeting_text:
            print(greeting_string)

    def generate_txt_file(self):
        self.get_filename()
        while not self.txt_generated:
            print("Enter function for y(x) (for ex sin(x))\n----> ")
            self.talk()
            self.txt_generated = True

    def get_filename(self):
        print("\nEnter a name for the new file (without .txt): ")
        self.file_name = input()
        self.file_name += '.txt'
        print(f"OK. The future file name is {self.file_name}\n")

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
