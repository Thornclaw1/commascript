import sys

from condense_file import flatten


class StringIterator:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0]

    def advance(self, amount=1):
        self.pos += amount
        self.current_char = self.text[self.pos] if self.pos >= len(self.text) else None


def expand(str):
    str_iter = StringIterator(str)
    new_str = ""

    # New expand code here

    return new_str


def main():
    if len(sys.argv) <= 1:
        print("Unspecified file")
        return

    file_path = sys.argv[1]
    output_file_path = sys.argv[2] if len(sys.argv) > 2 else file_path
    file_contents = ""
    with open(file_path) as file:
        file_contents = file.read()

    file_contents = flatten(file_contents)
    file_contents = expand(file_contents)

    with open(output_file_path, 'w') as file:
        file.write(file_contents)


main()
