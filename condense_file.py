import sys


def flatten(str):
    # return "".join(str.split())
    new_str = ""
    in_string = False
    in_comment = False
    opening_quote = ''
    for char in str:
        if char == '#' and not in_string:
            in_comment = not in_comment
            continue
        if in_comment:
            continue
        if in_string or not char.isspace():
            new_str += char
            if char in '"\'':
                if in_string:
                    if opening_quote == char:
                        in_string = False
                        opening_quote = ''
                else:
                    in_string = True
                    opening_quote = char
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
    with open(output_file_path, 'w') as file:
        file.write(file_contents)


main()
