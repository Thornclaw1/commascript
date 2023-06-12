import sys

from condense_file import flatten


def expand(str):
    indent = 0
    angle_depth = 0
    new_str = ""

    # def newline():
    #     new_str += "\n" + "\t" * indent

    for c in str:
        if c == '<':
            angle_depth += 1
        elif c == '>':
            angle_depth -= 1
        elif c == ';':
            indent -= 1
            new_str += "\n" + "\t" * indent

        new_str += c

        if c == ':':
            indent += 1
            new_str += "\n" + "\t" * indent
            continue
        if c == ',':
            if angle_depth == 0:
                new_str += "\n" + "\t" * indent
            continue

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
