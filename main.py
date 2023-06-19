# Sakib Ahmed
# A compiler that can parse my own programming language

# imports
import os
import sys

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


def ParseLine(line):
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


def MakeIndent():
    global numIndents
    indent = "    "
    return indent * numIndents


def ParseBlock(line):
    global numIndents
    while line != "}":
        if line == "{":
            line = origFile.readline().strip()
            continue
        else:
            # compFile.write(MakeIndent(numIndents))
            ParseLine(line)
            compFile.write("\n")
        line = origFile.readline().strip()


def Copy(line):
    global numIndents
    compFile.write(MakeIndent() + line)


def For(line):
    global numIndents

    params = line[line.index("(") + 1:line.index(")")].split(",")
    for i in range(3):
        params[i] = params[i].strip()

    # compFile = open(compPath, "a")
    # with open(compPath, "a") as compFile:
    compFile.write(MakeIndent() + params[0] + "\n")
    compFile.write(MakeIndent() + f"while {params[1]}:\n")

    numIndents += 1

    line = origFile.readline().strip()
    ParseBlock(line)
    compFile.write(MakeIndent() + params[2] + "\n")

    numIndents -= 1


def ForEach(line):
    global numIndents

    params = line[line.index("(") + 1:line.index(")")].strip().split(":")
    for i in range(2):
        params[i] = params[i].strip()

    # with open(compPath, "a") as compFile:
    compFile.write(MakeIndent() + f"for {params[0]} in {params[1]}:\n")

    numIndents += 1

    line = origFile.readline().strip()
    ParseBlock(line)

    numIndents -= 1


def While(line):
    global numIndents

    param = line[line.index("(") + 1:line.index(")")].strip()

    compFile.write(MakeIndent() + f"while {param}:\n")

    numIndents += 1

    line = origFile.readline().strip()
    ParseBlock(line)

    numIndents -= 1


def Function(line):
    global numIndents
    nameParams = line[line.index(" "):line.index(")") + 1].strip()

    compFile.write(f"def {nameParams}:\n")

    numIndents += 1

    line = origFile.readline().strip()
    ParseBlock(line)

    numIndents -= 1


# parse each line from the original file
for line in origFile:
    # for i in SyntaxChecker.Tokenizer(line):
    #     print(i.type, i.val, end=", ")
    # print()
    ParseLine(line)


# close the original and compiled files
origFile.close()
compFile.close()

# Execute everything from the newly "compiled" file
with open("temp.py") as file:
    # print(file.read())
    exec(file.read())

# remove the temporary file
# os.remove("temp.py")
