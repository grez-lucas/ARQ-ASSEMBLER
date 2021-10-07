import re

class bcolors:
    OK = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

#file_name = input("Ingrese el nombre del archivo:")
file_name = "p3_1-correccion1"

hexadecimal = r'#[A-F\d]{0,2}'
literal = rf'(\d+|[B-Z]\w+|{hexadecimal})' #A is exclusive for regA
dir = rf'\({literal}\)'

instructions={r"\b(MOV)\s":{r'\s(A\s*,\s*B)\s':'0000000',r'\s(B\s*,\s*A)\s':'0000001',rf'\s(A\s*,\s*{literal})\s':'0000010',rf'\s(B\s*,\s*{literal})\s':'0000011',rf'\s(A\s*,\s*{dir})\s':'0100101',rf'\s(B\s*,\s*{dir})\s':'0100110',rf'\s({dir}\s*,\s*A)\s':'0100111',rf'\s({dir}\s*,\s*B)\s':'0101000',r'\s(A\s*,\s*\(B\))\s':'0101001',r'\s(B\s*,\s*\(B\))\s':'0101010',r'\s(\(B\)\s*,\s*A)\s':'0101011'},
     r"\b(ADD)\s":	{r'\s(A\s*,\s*B)\s':'0000100',r'\s(B\s*,\s*A)\s':'0000101',rf'\s(A\s*,\s*{literal})\s':'0000110',rf'\s(B\s*,\s*{literal})\s':'0000111',rf'\s(A\s*,\s*{dir})\s':'0101100',rf'\s(B\s*,\s*{dir})\s':'0101101',rf'\s(A\s*,\s*\(B\))\s':'0101110',rf'\s({dir})\s':'0101111'},
     r"\b(AND)\s":	{r'\s(A\s*,\s*B)\s':'0001100',r'\s(B\s*,\s*A)\s':'0001101',rf'\s(A\s*,\s*{literal})\s':'0001110',rf'\s(B\s*,\s*{literal})\s':'0001111',rf'\s(A\s*,\s*{dir})\s':'0101100',rf'\s(B\s*,\s*{dir})\s':'0101101',rf'\s(A\s*,\s*\(B\))\s':'0101110',rf'\s({dir})\s':'0101111'},
     r"\b(SUB)\s":	{r'\s(A\s*,\s*B)\s':'0001000',r'\s(B\s*,\s*A)\s':'0001001',rf'\s(A\s*,\s*{literal})\s':'0001010',rf'\s(B\s*,\s*{literal})\s':'0001011',rf'\s(A\s*,\s*{dir})\s':'0110000',rf'\s(B\s*,\s*{dir})\s':'0110001',rf'\s(A\s*,\s*\(B\))\s':'0110010',rf'\s({dir})\s':'0110011'},
     r"\b(OR)\s":	{r'\s(A\s*,\s*B)\s':'0010000',r'\s(B\s*,\s*A)\s':'0010001',rf'\s(A\s*,\s*{literal})\s':'0010010',rf'\s(B\s*,\s*{literal})\s':'0010011',rf'\s(A\s*,\s*{dir})\s':'0111000',rf'\s(B\s*,\s*{dir})\s':'0111001',rf'\s(A\s*,\s*\(B\))\s':'0111010',rf'\s({dir})\s':'0111011'},
     r"\b(NOT)\s":	{r'\s(A\s*,\s*A)\s':'0010100',r'\s(A\s*,\s*B)\s':'0010101',r'\s(B\s*,\s*A)\s':'0010110',r'\s(B\s*,\s*B)\s':'0010111',rf'\s({dir}\s*,\s*A)\s':'0111100',rf'\s({dir}\s*,\s*B)\s':'0111101',r'\s(\(B\))\s':'0111110'},
     r"\b(XOR)\s":	{r'\s(A\s*,\s*B)\s':'0011000',r'\s(B\s*,\s*A)\s':'0011001',rf'\s(A\s*,\s*{literal})\s':'0011010',rf'\s(B\s*,\s*{literal})\s':'0011011',rf'\s(A\s*,\s*{dir})\s':'0111111',rf'\s(B\s*,\s*{dir})\s':'1000000',rf'\s(A\s*,\s*\(B\))\s':'1000001',rf'\s({dir})\s':'1000010'},
     r"\b(SHL)\s":	{r'\s(A\s*,\s*A)\s':'0011100',r'\s(A\s*,\s*B)\s':'0011101',r'\s(B\s*,\s*A)\s':'0011110',r'\s(B\s*,\s*B)\s':'0011111',rf'\s({dir}\s*,\s*A)\s':'1000011',rf'\s({dir}\s*,\s*B)\s':'1000100',r'\s(\(B\))\s':'1000101'},
     r"\b(SHR)\s":	{r'\s(A\s*,\s*A)\s':'0100000',r'\s(A\s*,\s*B)\s':'0100001',r'\s(B\s*,\s*A)\s':'0100010',r'\s(B\s*,\s*B)\s':'0100011',rf'\s({dir}\s*,\s*A)\s':'1000110',rf'\s({dir}\s*,\s*B)\s':'1000111',r'\s(\(B\))\s':'1001000'},
     r"\b(INC)\s":	{r'\s(B)\s':'0100100',rf'\s({dir})\s':'1001001',r'\s(\(B\))\s':'1001010'},
     r"\b(RST)\s":	{rf'\s({dir})\s':'1001011',r'\s(\(B\))\s':'1001100'},
     r"\b(CMP)\s":	{r'\s(A\s*,\s*B)\s':'1001101',rf'\s(A\s*,\s*{literal})\s':'1001110',rf'\s(B\s*,\s*{literal})\s':'1001111',rf'\s(A\s*,\s*{dir})\s':'1010000',rf'\s(B\s*,\s*{dir})\s':'1010001',rf'\s(A\s*,\s*\(B\))\s':'1010010'}, #revisar como evitar que se haga CMP B,(A)
     r"\b(JMP)\s":	{rf'\s({literal})\s':'1010011'},
     r"\b(JEQ)\s":	{rf'\s({literal})\s':'1010100'},
     r"\b(JNE)\s":	{rf'\s({literal})\s':'1010101'},
     r"\b(JGT)\s":	{rf'\s({literal})\s':'1010110'},
     r"\b(JLT)\s":	{rf'\s({literal})\s':'1010111'},
     r"\b(JGE)\s":	{rf'\s({literal})\s':'1011000'},
     r"\b(JLE)\s":	{rf'\s({literal})\s':'1011001'},
     r"\b(JCR)\s":	{rf'\s({literal})\s':'1011010'},
     r"\b(JOV)\s":	{rf'\s({literal})\s':'1011011'},
     r"\b(CALL)\s":   {rf'\s({dir})\s':'1010011'},#revisar si toma (Dir) o Dir
     r"\b(RET)\s":	{r'^\s*':'1010100'},
     r"\b(PUSH)\s":   {r'\s(A)\s':'1010101',r'\s(B)\s':'1010110'},
     r"\b(POP)\s" :   {r'\s(A)\s':'1010111',r'\s(B)\s':'1011000'}
     }


def validate_pattern(dictionary,row):
     for key in dictionary:#key (regular expression) we want to validate in our row
          pattern = re.compile(key)
          match = pattern.search(row)
          if match:
               valid=True
               
               return valid,key,match.group(0)
          else:
               valid = False

     return valid,key,None#returns bool, the key that was identified & match object

with open(file_name+".ass") as file:
     with open(file_name+".out",mode='w') as out_file:

          row_counter, valid_row_counter = 0 , 0
          fileIsValid = True
          for row in file:

               #validate instruction
               instruction_valid,instruction_str,instruction_regexp_group = validate_pattern(instructions,row)
               #validate operands
               operands_valid,operands_str,operands_regexp_group = validate_pattern(instructions[instruction_str],row)

               if instruction_valid == False:
                    print(f'{bcolors.FAIL}{row[:-1]}    \t\tInvalid Instruction{bcolors.ENDC}')
               elif instruction_valid == True and operands_valid == False:
                    print(f'{bcolors.FAIL}{row[:-1]}    \t\tInvalid Operands{bcolors.ENDC}')
               else:
                    print(f'{bcolors.OK}{row[:-1]}      \t\tValid Instruction{bcolors.ENDC}')
                    valid_row_counter+=1
               
               row_counter+=1
               # print(row,
               # "\n\tinstructionIsValid: ",instruction_valid,
               # "\n\tinstructionGroup: ",instruction_regexp_group,
               # "\n\toperandsValid: ",operands_valid,
               # "\n\toperandsLine: ",operands_str,
               # "\n\toperandsGroup: ", operands_regexp_group)
               if fileIsValid == True:
                    out_file.write(instructions[instruction_str][operands_str])
                    out_file.write("\n")
               if valid_row_counter != row_counter:
                    fileIsValid = False
          
          if fileIsValid == False:
               print(f"\n{bcolors.FAIL}ERROR:  Couldn't assemble code -->\n\tOne or more lines are invalid{bcolors.ENDC}")
          else:
               print(f"\n{bcolors.OK}SUCCESS:  Code assembled successfully{bcolors.ENDC}")
          out_file.close()



