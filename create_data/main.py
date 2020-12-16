class DataCreate:
    def __init__(self):
        self.greeting_text = []
        with open('greeting.txt', 'r') as greeting_file:
            for string in greeting_file:
                self.greeting_text.append(string.strip())
        self.txt_generated = False
        self.is_active = True

    def greeting(self):
        for greeting_string in self.greeting_text:
            print(greeting_string)

    def generate_txt_file(self):
        while not self.txt_generated:
            self.talk()

    def talk(self):
        pass


def main():
    data_create = DataCreate()
    data_create.greeting()
    data_create.generate_txt_file()


if __name__ == "__main__":
    main()
