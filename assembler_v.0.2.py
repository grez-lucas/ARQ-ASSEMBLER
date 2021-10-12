import re

class clrPrint():
    @staticmethod
    def okPrint(value,value2):
        print(f'\033[92m{value:<30}\t\t{value2:<40}\033[0m')
    
    @staticmethod
    def failPrint(value,value2):
        print(f'\033[91m{value:<30}\t\t{value2:<40}\033[0m')

#file_name = input("Enter the file's name: ")
file_name = "p3_2-correccion2"

label = r'^([a-zA-Z]\w+|[^AB,\.\(\)]):$' #A & B are exclusive for regA, regB
variable = r'([a-zA-Z]\w+|[^AB,\(\)\s\d\.])' #A & B are exclusive for regA, regB
binary = r'[0-1]{1,8}'
hexadecimal = r'#([A-F\d]{0,2})'
decimal = r'(-?25[0-5]|-?2[0-5]\d|-?1\d{1,2}|-?\d{1,2})'
literal = rf'({decimal}|{hexadecimal}|{variable})'
dir = rf'\({literal}\)'



valid_data_values = {r'\s([a-zA-Z]+|[^AB])\s':rf'\s({decimal}|{hexadecimal})\s'}

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
     r"\b(CALL)\s": {rf'\s({dir})\s':'1010011'},#revisar si toma (Dir) o Dir
     r"\b(RET)\s":	{r'^\s*':'1010100'},
     r"\b(PUSH)\s": {r'\s(A)\s':'1010101',r'\s(B)\s':'1010110'},
     r"\b(POP)\s" : {r'\s(A)\s':'1010111',r'\s(B)\s':'1011000'}
     }


def toBin(value):
     dec_match = (re.compile(decimal)).search(value)
     hex_match = (re.compile(hexadecimal)).search(value)
     if hex_match:
          return bin(int(hex_match.group(1), base=16))[2:].zfill(8)
     elif dec_match:
          return bin(int(dec_match.group(1)))[2:].zfill(8)
     else:
          return False
     
def validate_pattern(data,row):
     if isinstance(data,dict) or isinstance(data,list):
          if len(data) == 0:
               return False,data,None
          for key in data:              #key (regular expression) we want to validate in our row
               pattern = re.compile(key)
               match = pattern.search(row)
               if match:
                    valid=True
                    
                    return valid,key,match.group(1)
          else:
               return False,key,None
     else:
          pattern = re.compile(data)
          match = pattern.search(row)
          if match:
               valid = True
               return valid,data,match.group(1)


     return False,data,None   #returns bool, the key that was identified & match object


def regex_find_span(text,word):
     pattern = re.compile(word)
     match = pattern.search(text)
     if match:
          return match.span() #returns the index span of a word in a text as list
     else:
          return None

with open(file_name+".ass") as file:

     contents = file.read()
     code_span = regex_find_span(contents,r'\bCODE:\n')
     data_span = regex_find_span(contents,r'\bDATA:\n')
     data_variables = {}
     
     #write .mem file. It must have the initial DATA: Block variables saved in it
     if data_span:
          with open(file_name+".mem",mode='w') as mem_file: #READ DATA BLOCK

               file.seek(data_span[1])          #begin reading from DATA:\n onwards
               row_counter, valid_row_counter = 0 , 0
               fileIsValid = True
               
               for row in file:
                    
                    if row == "CODE:\n":
                         break
                    if row == r'^\s+\n$':       #if row is empty, continue to the next iteration
                         continue
                    
                    #validate data
                    data_valid,data_str,data_regexp_group = validate_pattern(valid_data_values,row)
                    #validate data_value
                    value_valid,value_str,value_regexp_group = validate_pattern(valid_data_values[data_str],row)

                    if data_valid == False:
                         clrPrint.failPrint(row[:-1],"Invalid Variable Name")
                    elif data_valid == True and value_valid == False:
                         clrPrint.failPrint(row[:-1],"Value Must be Hex or Dec")
                    else:
                         clrPrint.okPrint(row[:-1],"Valid Instruction")
                         data_variables[rf'({data_regexp_group})'] = value_regexp_group
                         valid_row_counter +=1
 
                    row_counter +=1

                    if valid_row_counter != row_counter:
                         fileIsValid = False

                    if fileIsValid == True:

                         mem_file.write(toBin(value_regexp_group))
                         mem_file.write("\n")

          #READ LABELS
          labels = [] 
          file.seek(code_span[1]) #start reading from CODE: onward
          for row in file:
               if (re.compile(label).search(row)):     #if row is LABEL: -> begin label comprehension
                    match = re.compile(label).search(row)
                    labels.append(rf'({match.group(1)})')


     with open(file_name+".out",mode='w') as out_file: #READ CODE BLOCK


          if code_span:
               file.seek(code_span[1])                 #start right after CODE:, use regex_find_span to find position
          else:
               file.seek(0)                            #file has no code or data block, start reading from the beggining      

          row_counter, valid_row_counter = 0 , 0
          fileIsValid = True

          for row in file:
               if row == r'^\s+\n$':                   #if row is empty, continue to the next iteration
                    continue
               
               if (re.compile(label).search(row)):     #if row is LABEL: -> 
                    clrPrint.okPrint(row[:-1],"Valid Label")
                    continue


               #validate instruction
               instruction_valid,instruction_str,instruction_regexp_group = validate_pattern(instructions,row)
               #validate operands
               operands_valid,operands_str,operands_regexp_group = validate_pattern(instructions[instruction_str],row)

               if instruction_valid == False:
                    clrPrint.failPrint(row[:-1],"Invalid Instruction")
               elif instruction_valid == True and operands_valid == False:
                    clrPrint.failPrint(row[:-1],"Invalid Operands")
               else:
                    if instruction_str in list(instructions.keys())[12:20] and data_span:#if the instruction is a jump, check if the operand is a valid label
                         label_valid,label_str,label_regexp_group = validate_pattern(labels,row)
                         if label_valid == False:
                              clrPrint.failPrint(row[:-1],"Invalid Label Name")
                              row_counter+=1
                              continue
                         else:
                              clrPrint.okPrint(row[:-1],"Valid Jump")
                              out_file.write(instructions[instruction_str][operands_str])
                              out_file.write(''.zfill(8))
                              out_file.write("\n")
                              continue


                    if (re.compile(literal).search(operands_regexp_group)):#if one of the operands is a hex, dec or variable, check if it's valid
                         if (re.compile(hexadecimal).search(operands_regexp_group)) or (re.compile(decimal).search(operands_regexp_group)):#hex & dec block
                              clrPrint.okPrint(row[:-1],"Valid Instruction")
                              valid_row_counter+=1
                              row_counter+=1
                              out_file.write(instructions[instruction_str][operands_str])
                              out_file.write(toBin(operands_regexp_group))
                              out_file.write("\n")
                              continue

                         else:          #variable block
                              valid_variable,variable_str,variable_regexp_group =  validate_pattern(data_variables, operands_regexp_group)
                              if valid_variable == False:
                                   clrPrint.failPrint(row[:-1],"Invalid Variable name")
                              else:
                                   clrPrint.okPrint(row[:-1],"Valid Instruction")
                                   valid_row_counter+=1
                                   row_counter+=1
                                   out_file.write(instructions[instruction_str][operands_str])
                                   #read data_varables
                                   out_file.write(toBin(data_variables[variable_str]))
                                   out_file.write("\n")
                                   continue
                    
                    
                    else:
                         clrPrint.okPrint(row[:-1],"Valid Instruction")
                         valid_row_counter+=1
               

               row_counter+=1

               if fileIsValid == True:
                    out_file.write(instructions[instruction_str][operands_str])
                    out_file.write(''.zfill(8))
                    out_file.write("\n")
               if valid_row_counter != row_counter:
                    fileIsValid = False
          
          if fileIsValid == False:
               clrPrint.failPrint("\n","ERROR:  Couldn't assemble code -->\n\tOne or more lines are invalid")
          else:
               clrPrint.okPrint("\n","SUCCESS:  Code assembled successfully")
          