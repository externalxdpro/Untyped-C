# Sakib Ahmed
# A compiler that can parse my own programming language

# imports
import os
import sys
import SyntaxChecker

# set path of original file from command line args
n = len(sys.argv)
if n > 1:
    origPath = sys.argv[1]
else:
    origPath = r"test.uc"

# set path of compiled file
compPath = r"temp.py"

# open both files
origFile = open(origPath, "r")
compFile = open(compPath, "w")

# set num of indents
numIndents = 0


def MakeIndent():
    """Create the specified number of indents."""
    # allow access to the global variable
    global numIndents
    # set the number of spaces in one indent
    indent = "    "
    # multiply the spaces to create the specified number of indents
    return indent * numIndents


def Copy(line):
    """Directly copy a line from original file to compiled file."""
    # allow access to the global variable
    global numIndents
    # write the line from the original file to the compiled file
    # with indents before it
    compFile.write(MakeIndent() + line)


def For(line):
    """Convert for loop in original file to compiled file."""
    # allow access to the global variable
    global numIndents

    # get the parameters for the for loop inbetween the brackets
    params = line[line.index("(") + 1:line.index(")")].split(",")

    # strip each parameter
    for i in range(3):
        params[i] = params[i].strip()

    # add the first parameter
    # and the second parameter in a while loop
    # with indents
    compFile.write(MakeIndent() + params[0] + "\n")
    compFile.write(MakeIndent() + f"while {params[1]}:\n")

    # indent for the block of code under the while loop
    numIndents += 1

    # get the next line from the origfile
    line = origFile.readline().strip()
    # parse every line in the block
    ParseBlock(line)
    # add the second third parameter at the end of the while loop
    compFile.write(MakeIndent() + params[2] + "\n")

    # unindent at the end of the block
    numIndents -= 1


def ForEach(line):
    """Convert for-each loop in original file to compiled file."""
    # allow access to the global variable
    global numIndents

    # get the parameters for the for-each loop inbetween the brackets
    params = line[line.index("(") + 1:line.index(")")].strip().split(":")

    # strip each parameter
    for i in range(2):
        params[i] = params[i].strip()

    # write the for loop into the compfile
    compFile.write(MakeIndent() + f"for {params[0]} in {params[1]}:\n")

    # indent for the block under the for loop
    numIndents += 1

    # read the next line from the origfile
    line = origFile.readline().strip()
    # parse every line under the for loop
    ParseBlock(line)

    # unindent after the block
    numIndents -= 1


def While(line):
    """Convert while loop in original file to compiled file."""
    # allow access to the global variable
    global numIndents

    # get the parameter for the while loop inbetween the brackets
    param = line[line.index("(") + 1:line.index(")")].strip()

    # write the parameter into the compfile
    compFile.write(MakeIndent() + f"while {param}:\n")

    # indent for the block under the while loop
    numIndents += 1

    # read the next line from the origfile
    line = origFile.readline().strip()
    # parse every line in the block under the while loop
    ParseBlock(line)

    # unindent after the end of the while loop
    numIndents -= 1


def Function(line):
    """Convert function declaration in original file to compiled file."""
    # allow access to the global variable
    global numIndents
    # get the name of the function and the parameters of the function
    nameParams = line[line.index(" "):line.index(")") + 1].strip()

    # write the name and the parameters into the compfile
    compFile.write(f"def {nameParams}:\n")

    # indent for the body of the function
    numIndents += 1

    # read the next line from the origfile
    line = origFile.readline().strip()
    # parse the body of the function
    ParseBlock(line)

    # unindent after the body of the function
    numIndents -= 1


def ParseLine(line):
    """Parse the inputted line depending on what it contains."""
    # depending on the contents of the line, run the corresponding function
    if "for" in line:
        if ":" in line:
            ForEach(line)
        else:
            For(line)
    elif "while" in line:
        While(line)
    elif "fn" in line:
        Function(line)
    elif line != "":
        Copy(line)


def ParseBlock(line):
    """Parse the body of a for, for-each, while and function declaration."""
    # allow access to the global variable
    global numIndents

    # run until the closing curly bracket
    while line != "}":
        # if the line only contains an opening curly bracket
        # go to the next line
        if line == "{":
            line = origFile.readline().strip()
            continue
        else:
            # parse each line and create a newline
            ParseLine(line)
            compFile.write("\n")
        # read the next line
        line = origFile.readline().strip()


# check syntax and parse each line from the original file
for line in origFile:
    SyntaxChecker.SyntaxChecker(line)
    ParseLine(line)

# close the original and compiled file
origFile.close()
compFile.close()

# Execute everything from the newly "compiled" file
with open("temp.py") as file:
    exec(file.read())

# remove the temporary file
os.remove("temp.py")
