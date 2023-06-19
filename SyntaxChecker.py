import string


class Token():
    def __init__(self, type: str, val: str):
        self.type = type
        self.val = val


def Tokenizer(line):
    tokens = []

    cur = 0
    while cur < len(line):
        char = line[cur]
        type = ""

        if char == "(" or char == ")" or char == "{" or char == "}" or char == "[" or char == "]":
            type = "paren"
        elif char == "," or char == ";":
            type = "seperator"
        elif char == ":":
            type = "colon"
        elif char == "=":
            if cur != len(line) - 1 and line[cur + 1] == "=":
                cur += 1
                char += line[cur]
                type = "condition"
            else:
                type = "assignment"
        elif char == "+" or char == "-":
            if cur != len(line) - 1:
                if line[cur + 1] == "=":
                    cur += 1
                    char += line[cur]
                    type = "assignment"
                if line[cur + 1].isdigit():
                    num = ""
                    while char.isdigit():
                        num += char
                        cur += 1
                        char = line[cur]
                    tokens.append(Token("number", num))
                    continue
            else:
                type = "math"
        elif char == "<" or char == ">":
            if cur != len(line) - 1 and line[cur + 1] == "=":
                cur += 1
                char += line[cur]
            type = "condition"
        elif char == "!":
            if cur != len(line) - 1 and line[cur + 1] == "=":
                cur += 1
                char += line[cur]
                type = "condition"
        elif char.isdigit():
            num = ""
            while char.isdigit():
                num += char
                cur += 1
                char = line[cur]

            tokens.append(Token("number", num))
            continue
        elif char in string.ascii_letters:
            name = ""
            while char in string.ascii_letters:
                name += char
                cur += 1
                char = line[cur]

            tokens.append(Token("name", name))
            continue
        elif char == "\"":
            name = ""

            while True:
                name += char
                cur += 1
                char = line[cur]
                if char == "\"":
                    name += line[cur]
                    cur += 1
                    break

            tokens.append(Token("string", name))
            continue
        elif char == " " or char == "\n":
            cur += 1
            continue

        if type == "":
            raise SyntaxError(f"Unknown character: {char} in line: \n {line}")

        tokens.append(Token(type, char))
        cur += 1

    return tokens


def SyntaxChecker(line):
    tokens = Tokenizer(line)

    if len(tokens) == 0:
        return

    first = tokens[0]
    if first.type == "name":
        # Handles for and foreach
        if first.val == "for":
            if ":" in line:
                if len(tokens) != 6 and len(tokens) != 7:
                    raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
                syntax = ["name", "paren", "name", "colon", "name", "paren", "paren"]

                for i in range(0, 5):
                    if tokens[i].type != syntax[i]:
                        print(tokens[i].type, tokens[i].val)
                        raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
            else:
                if len(tokens) != 14 and len(tokens) != 15:
                    raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
                syntax = ["name", "paren", "name", "assignment", "number",
                          "seperator", "name", "condition", "number",
                          "seperator", "name", "assignment", "number", "paren", "paren"]

                for i in range(0, 13):
                    if tokens[i].type != syntax[i]:
                        print(tokens[i].type, tokens[i].val)
                        raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
        elif first.val == "while":
            if len(tokens) != 6 and len(tokens) != 7:
                raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
            syntax = ["name", "paren", "name", "condition", "number", "paren", "paren"]

            for i in range(0, 5):
                if tokens[i].type != syntax[i]:
                    print(tokens[i].type, tokens[i].val)
                    raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
