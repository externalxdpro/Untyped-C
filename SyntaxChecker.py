"""A tokenizer and kinda trash syntax checker."""

# imports
import string


# An object containing data for a token
# Has a type and a value
class Token():
    """Type for a token."""

    def __init__(self, type: str, val: str):
        """Initialize a token with type and value."""
        self.type = type
        self.val = val


def Tokenizer(line):
    """Tokenize the inputted line."""
    # create an empty list of the tokens in the line
    tokens = []

    # index for the current character in the line
    cur = 0
    # keep looping until the end of the line
    while cur < len(line):
        # set the character with the index
        char = line[cur]
        # set type to none
        type = None

        # if the character is any type of bracket, set the type to paren (parentheses)
        if char == "(" or char == ")" or char == "{" or char == "}" or char == "[" or char == "]":
            type = "paren"
        # a comma and semicolon will be set to type seperator
        elif char == "," or char == ";":
            type = "seperator"
        # a colon would be of type colon
        elif char == ":":
            type = "colon"
        # if the character is an equals sign
        elif char == "=":
            # if the next character is an equal sign,
            # advance the index, and combine them into one string
            # and set to type condition
            if cur != len(line) - 1 and line[cur + 1] == "=":
                cur += 1
                char += line[cur]
                type = "condition"
            # it would be an assignment if there is no second equals sign
            else:
                type = "assignment"
        # if the character is a plus/minus/asterisk, the type can be
        # assignment or number depending on what characters follow it
        elif char == "+" or char == "-" or char == "*":
            # if there is an equals sign after, it is an assignment operator
            if cur != len(line) - 1 and line[cur + 1] == "=":
                cur += 1
                char += line[cur]
                type = "assignment"
            # if there is a number after, the type is number
            elif cur != "*" and cur != len(line) - 1 and line[cur + 1].isdigit():
                num = char
                cur += 1
                char = line[cur]
                while char.isdigit():
                    num += char
                    cur += 1
                    char = line[cur]
                # add the token to the list and continue
                tokens.append(Token("number", num))
                continue
            # if there is nothing after, the type is math
            else:
                type = "math"
        # if the character is a slash, then the line should be
        # a comment, an assignment, or a math operator
        elif char == "/":
            # if the next character is a slash, then the line is a comment
            if cur != len(line) - 1 and line[cur + 1] == "/":
                tokens.append(Token("comment", line.strip()))
                break
            # if the next character is an equals sign, then it is assignment
            elif cur != len(line) - 1 and line[cur + 1] == "=":
                cur += 1
                char += line[cur]
                type = "assignment"
            # if there is neither of those after, then the type is math
            else:
                type = "math"
        # if the character is a greater/less than sign
        # the type will be condition
        elif char == "<" or char == ">":
            # if there is an equals sign after,
            # that will be a part of the token as well
            if cur != len(line) - 1 and line[cur + 1] == "=":
                cur += 1
                char += line[cur]
            type = "condition"
        # if the character is an exclamation mark with an equals sign after,
        # then the type is condition
        elif char == "!":
            if cur != len(line) - 1 and line[cur + 1] == "=":
                cur += 1
                char += line[cur]
                type = "condition"
        # if the character is a digit, then the type is number
        elif char.isdigit():
            # keep advancing the index to check for any digits after the current index
            num = ""
            while char.isdigit():
                num += char
                cur += 1
                char = line[cur]

            # add the token to the list and continue
            tokens.append(Token("number", num))
            continue
        # if the character is a letter, the type is a name
        # (could be the name of a function or a variable)
        elif char in string.ascii_letters:
            # keep advancing the index to check for any letters after the current index
            name = ""
            while char in string.ascii_letters or char.isdigit():
                name += char
                cur += 1
                char = line[cur]

            # add the token to the list and continue
            tokens.append(Token("name", name))
            continue
        # if the character is a quotation mark, then it must be a string
        elif char == "\"":
            name = ""

            # keep advancing the pointer until the closing quotation mark is found
            # meaning the end of the string
            while True:
                name += char
                cur += 1
                char = line[cur]
                if char == "\"":
                    name += line[cur]
                    cur += 1
                    break

            # add the token to the list and continue
            tokens.append(Token("string", name))
            continue
        # if the character is a space or a line break then
        # advance the index and continue
        elif char == " " or char == "\n":
            cur += 1
            continue

        # if the type is none, there is an unknown character in the line
        if type is None:
            raise SyntaxError(f"Unknown character: {char} in line: \n {line}")

        # add the token to the list and advance the index
        tokens.append(Token(type, char))
        cur += 1

    # return the list of tokens
    return tokens


def SyntaxChecker(line):
    """Check syntax for a line."""
    # get a list of tokens for the passed-in line
    tokens = Tokenizer(line)

    # if there are no tokens, exit the function
    if len(tokens) == 0:
        return

    # the first token will be a name of a variable, or a keyword
    first = tokens[0]
    if first.type == "name":
        # checks syntax for a for/foreach loop
        if first.val == "for":
            # if there is a colon in the line, it is a foreach loop
            if ":" in line:
                # the number of tokens must be 6 or 7
                if len(tokens) != 6 and len(tokens) != 7:
                    raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
                # specifies the order of the token types in a foreach loop
                syntax = ["name", "paren", "name", "colon", "name", "paren", "paren"]

                # loop through the lists and check if there are any inequalities
                # if there is, there is a syntax error
                for i in range(0, 5):
                    if tokens[i].type != syntax[i]:
                        print(tokens[i].type, tokens[i].val)
                        raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
            else:
                if len(tokens) != 14 and len(tokens) != 15:
                    raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
                # specifies the order of the token types in a for loop
                syntax = ["name", "paren", "name", "assignment", "number",
                          "seperator", "name", "condition", "number",
                          "seperator", "name", "assignment", "number", "paren", "paren"]

                # loop through the lists and check if there are any inequalities
                # if there is, there is a syntax error
                for i in range(0, 13):
                    if tokens[i].type != syntax[i]:
                        print(tokens[i].type, tokens[i].val)
                        raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
        # checks syntax for a while loop
        elif first.val == "while":
            # the number of tokens must be 6 or 7
            if len(tokens) != 6 and len(tokens) != 7:
                raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
            # specifies the order of the token types in a while loop
            syntax = ["name", "paren", "name", "condition", "number", "paren", "paren"]

            # loop through the lists and check if there are any inequalities
            # if there is, there is a syntax error
            for i in range(0, 5):
                if tokens[i].type != syntax[i]:
                    print(tokens[i].type, tokens[i].val)
                    raise SyntaxError(f"Incorrect syntax in line: \"{line}\"")
