# Symbol Table
# new labels encountered in first pass will be added to this table : "label_name": previous line number
table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    }
# loop to include R0,R1,R2,...R15 in the table
for i in range(0,16):
  R_num = "R" + str(i)
  table[R_num] = i

variablePointer = 16    # next available memory location(i.e. starting from 16) for new variables

# Dictionaries for components of C instruction
# Computation : c1 c2 c3 c4 c5 c6
comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }

# Destination : d1 d2 d3
dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }

#Jump : j1 j2 j3
jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


# strip func removes white spaces and comments from the line
# if it is a blank line it returns ""
def strip(line):
    c=0
    flag=0
    # loop to remove comments
    for i in line:
        c+=1
        if(i=='/'):
            flag=1
            ind=c
            break
    if flag==1:
        line=line[:ind-1]
    line.replace(" ","")     # removing white spaces
    if(line=="\n"):          # if it is a blank line it returns ""
      return ""
    else:
      return line

# general_C function converts a C instruction into the general format of C instruction
# adds null dest & jump fiels if they are not specified
def general_C(line):
  line = line[:-1]
  # adding dest field if not present
  if not "=" in line:
    line = "null=" + line
  # adding jump field if not present
  if not ";" in line:
    line = line + ";null"
  return line


# reads a symbolic A instruction and changes it into int if required
# converts the integer value to binary
def readA(line):
  if line[1].isalpha():    # checking if instruction is @variable_name or @numerical_value
    label = line[1:-1]
    var_value = table.get(label, -1)   
    if var_value == -1:    # if variable is not present in the symbol table 
      global variablePointer
      table[label] = variablePointer    # adding variable to symbol table
      variablePointer += 1
      var_value =table[label]
  else:
    var_value = int(line[1:])

  bin_value = bin(var_value)[2:].zfill(16)   # binary value of the var_value
  return bin_value
 
# reads a C instruction
def readC(line):
  line = general_C(line)
  parts_C = line.split("=")
  dest_code = dest.get(str(parts_C[0]), "destFAIL")   # d1 d2 d3
  parts_C = parts_C[1].split(";")
  comp_code = comp.get(str(parts_C[0]), "compFAIL")   # c1 c2 c3 c4 c5 c6
  jump_code = jump.get(str(parts_C[1]), "jumpFAIL")   # j1 j2 j3
  return comp_code,dest_code,jump_code                #returning a tuple of comp_code, dest_code & jump_code

# checks whether the instruction is A type or C type
# returns the binary format of the instruction
def read_instruction(line):
  if line[0] == "@":
    return readA(line)
  elif line[0]!="":
    parts = readC(line)
    return "111"+parts[0]+parts[1]+parts[2]

# coverts .asm file to a .txt file after removing white spaces, comments and blank lines
def firstPass(file_name):
  infile = open(file_name+".asm","r")
  outfile = open(file_name+ ".txt", "w")
  
  lineNumber = 0
  for line in infile:
    stripped_line = strip(line)
    if stripped_line != "":
      if stripped_line[0] == "(":
        label = stripped_line[1:-2]
        table[label] = lineNumber
        stripped_line = ""
      else:
        lineNumber += 1
        outfile.write(stripped_line)

  infile.close()
  outfile.close()

# reads instructions from .txt file and makes the corresponding .hack file 
def secondPass(file_name):
  infile = open(file_name + ".txt","r")
  outfile = open(file_name + ".hack", "w")

  for line in infile:
    instruction = read_instruction(line)
    outfile.write(instruction + "\n")

  infile.close()
  outfile.close()

# input file name (without file type ex.if file is pong.asm input="pong")
file_name=input()
firstPass(file_name)
secondPass(file_name)
