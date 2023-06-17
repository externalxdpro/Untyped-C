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


def ParseLine(line, numIndents=0):
    if "for" in line:
        if ":" in line:
            ForEach(line, numIndents)
        else:
            For(line, numIndents)
    elif "while" in line:
        While(line, numIndents)
    elif "fn" in line:
        Function(line, numIndents)
    elif line != "":
        Copy(line, numIndents)


def MakeIndent(numIndents):
    indent = "    "
    return indent * numIndents


def ParseBlock(line, numIndents=0):
    while line != "}":
        if line == "{":
            line = origFile.readline().strip()
            continue
        else:
            compFile.write(MakeIndent(numIndents))
            ParseLine(line)
            compFile.write("\n")
        line = origFile.readline().strip()


def Copy(line, numIndents=0):
    compFile.write(MakeIndent(numIndents) + line)


def For(line, numIndents=0):
    params = line[line.index("(") + 1:line.index(")")].split(",")
    for i in range(3):
        params[i] = params[i].strip()

    # compFile = open(compPath, "a")
    # with open(compPath, "a") as compFile:
    compFile.write(params[0] + "\n")
    compFile.write(f"while {params[1]}:\n")
    numIndents += 1

    line = origFile.readline().strip()
    ParseBlock(line, numIndents)
    compFile.write(MakeIndent(numIndents) + params[2] + "\n")


def ForEach(line, numIndents=0):
    params = line[line.index("(") + 1:line.index(")")].strip().split(":")
    for i in range(2):
        params[i] = params[i].strip()

    # with open(compPath, "a") as compFile:
    compFile.write(f"for {params[0]} in {params[1]}:\n")
    numIndents += 1

    line = origFile.readline().strip()
    ParseBlock(line, numIndents)


def While(line, numIndents=0):
    param = line[line.index("(") + 1:line.index(")")].strip()

    compFile.write(f"while {param}:\n")
    numIndents += 1

    line = origFile.readline().strip()
    ParseBlock(line, numIndents)


def Function(line, numIndents=0):
    nameParams = line[line.index(" "):line.index(")") + 1].strip()

    compFile.write(f"def {nameParams}:\n")
    numIndents += 1

    line = origFile.readline().strip()
    ParseBlock(line, numIndents)


# parse each line from the original file
for line in origFile:
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