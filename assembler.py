import re  # * library to work with regex


# * prints in red for wrong output
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))


# * prints in cyan for debug
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))


# * prints in green for correct output
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))


# * Any 2, 3 or 4 letter word, one or more spaces and any character that's not a coma.
#! space_filter = r'[A-Z]{2,4}\s+[^,]'
# * any hexadecimal
hexadecimal = r'#(0|[1-9A-F][0-9A-F]*)'
# * any decimal negatives included
decimal = r'(0|[1-9]\d*|-[1-9]\d*)'
# * words (nletters >= 2) composed by any number of letter and/or underscores.
words = r'[a-zA-Z0-9_]{2,}'
# * single letter (any but A or B) or single underscore.
letter = r'[a-zC-Z0-9_]'
# * literal can be alphanumeric, numeric or just words mixed with underscore
lit = f'({words}|{letter}|({decimal}|{hexadecimal}))'
# * direction lit == (dir)
dir_lit = f'\({lit}\)'
# * labels any word ended with ':'  and can be preceeded by spaces
label = rf'^\s*({words}|{letter}):'
# * available instructions and its opcodes
instructions = {r'MOV': {r'^A,B$': '0000000', r'^B,A$': '0000001',
                         rf'^A,{lit}$': '0000010',
                         rf'^B,{lit}$': '0000011', rf'^A,{dir_lit}$': '0100101',
                         rf'^B,{dir_lit}$': '0100110', rf'^{dir_lit},A$': '0100111',
                         rf'^{dir_lit},B$': '0101000', r'^A,\(B\)$': '0101001',
                         r'^B,\(B\)$': '0101010', r'^\(B\),A$': '0101011'},
                r'ADD': {r'^A,B$': '0000100', r'^B,A$': '0000101',
                         rf'^A,{lit}$': '0000110', rf'^B,{lit}$': '0000111',
                         rf'^A,{dir_lit}$': '0101100', rf'^B,{dir_lit}$': '0101101',
                         r'^A,\(B\)$': '0101110', rf'^{dir_lit}$': '0101111'},
                r'SUB': {r'^A,B$': '0001000', r'^B,A$': '0001001',
                         rf'^A,{lit}$': '0001010', rf'^B,{lit}$': '0001011',
                         rf'^A,{dir_lit}$': '0110000', rf'^B,{dir_lit}$': '0110001',
                         r'^A,\(B\)$': '0110010', rf'^{dir_lit}$': '0110011'},
                r'AND': {r'^A,B$': '0001100', r'^B,A$': '0001101',
                         rf'^A,{lit}$': '0001110', rf'^B,{lit}$': '0001111',
                         rf'^A,{dir_lit}$': '0110100', rf'^B,{dir_lit}$': '0110101',
                         r'^A,\(B\)$': '0110110', rf'^{dir_lit}$': '0110111'},
                r'OR':  {r'^A,B$': '0010000', r'^B,A$': '0010001',
                         rf'^A,{lit}$': '0010010', rf'^B,{lit}$': '0010011',
                         rf'^A,{dir_lit}$': '0111000', rf'^B,{dir_lit}$': '0111001',
                         r'^A,\(B\)$': '0111010', rf'^{dir_lit}$': '0111011'},
                r'NOT': {r'^A,A$': '0010100', r'^A,B$': '0010101', r'^B,A$': '0010110',
                         r'^B,B$': '0010111', rf'^{dir_lit},A$': '0111100',
                         rf'^{dir_lit},B$': '0111101', rf'^\(B\)$': '0111110'},
                r'XOR': {r'^A,B$': '0011000', r'^B,A$': '0011001',
                         rf'^A,{lit}$': '0011010', rf'^B,{lit}$': '0011011',
                         rf'^A,{dir_lit}$': '0111111', rf'^B,{dir_lit}$': '1000000',
                         rf'^A,\(B\)$': '1000001', rf'^{dir_lit}$': '1000010'},
                r'SHL': {r'^A,A$': '0011100', r'^A,B$': '0011101', r'^B,A$': '0011110',
                         r'^B,B$': '0011111', rf'^{dir_lit},A$': '1000011', rf'^{dir_lit},B$': '1000100',
                         rf'^\(B\)$': '1000101'},
                r'SHR': {r'^A,A$': '0100000', r'^A,B$': '0100001', r'^B,A$': '0100010',
                         r'^B,B$': '0100011', rf'^{dir_lit},A$': '1000110', rf'^{dir_lit},B$': '1000111',
                         rf'^\(B\)$': '1001000'},
                r'INC': {r'^B$': '0100100', rf'^{dir_lit}$': '1001001', rf'^\(B\)$': '1001010'},
                r'RST': {rf'^{dir_lit}$': '1001011', rf'^\(B\)$': '1001100'},
                r'CMP': {r'^A,B$': '1001101', rf'^A,{lit}$': '1001110', rf'^B,{lit}$': '1001111',
                         rf'^A,{dir_lit}$': '1010000', rf'^B,{dir_lit}$': '1010001', rf'^A,\(B\)$': '1010010'},
                r'JMP': {rf'^{lit}$': '1010011'},
                r'JEQ': {rf'^{lit}$': '1010100'},
                r'JNE': {rf'^{lit}$': '1010101'},
                r'JGT': {rf'^{lit}$': '1010110'},
                r'JLT': {rf'^{lit}$': '1010111'},
                r'JGE': {rf'^{lit}$': '1011000'},
                r'JLE': {rf'^{lit}$': '1011001'},
                r'JCR': {rf'^{lit}$': '1011010'},
                r'JOV': {rf'^{lit}$': '1011011'},
                r'CALL': {rf'^{lit}$': '1011100'},
                r'RET': {rf'^\s*$': '1011101'},
                r'PUSH': {r'^\s*(A|B)$': '1011110'},
                r'POP': {r'^\s*(A|B)$': '1011111'}}  # TODO: test the four new instructions!
file_name = input('File name:')
instructions_file = open(f'{file_name}', 'r')
memory_file = open(f'{file_name[:-4]}' + '.mem', 'w')
opcodes_file = open(f'{file_name[:-4]}' + '.out', 'w')
# * keeps the line of the file that we are reading so we can display it in console afterwards (for debugging purposes)
line_number = 1
# * control signal
code = False
# * control signal
data = False
# * contains the labels found in the file
labels = []
# * contains the variables found in the file and it's value
variables = dict()
# * read the file once to save the labels as well as the variables so that we can check on them when they're referenced later
for lab in instructions_file:
    if len(lab.split()) == 0:  # * if the line is blank (filled with spaces) ignore it
        line_number += 1
        continue
    line_number += 1
    possible_lbl = lab.split()[0]
    pattern_label = re.compile(label)
    match_label = pattern_label.search(possible_lbl)
    if data:
        possible_data = lab.split()
        if len(possible_data) == 2:  # * if the variable has been initialized save it
            pattern_dec = re.compile(rf'^{decimal}$')
            pattern_hex = re.compile(rf'^{hexadecimal}$')
            match_dec = pattern_dec.search(possible_data[1])
            match_hex = pattern_hex.search(possible_data[1])
            if match_dec or match_hex:  # * if the number is right
                variables[possible_data[0]] = possible_data[1]
                if possible_data[1][0] == '#':
                    hex_dec = int(possible_data[1][1:], base=16)
                    num_bin = '{0:08b}'.format(hex_dec)
                else:
                    num_bin = '{0:08b}'.format(int(possible_data[1]))
                memory_file.write(str(num_bin) + '\n')
            else:
                prRed(
                    f'[Line {line_number}] invalid value for the variable: {possible_data[0]} ')
        # * if the variable hasn't been initialized
        elif len(possible_data) == 1 and possible_data[0] != 'CODE:':
            prRed(
                f'[Line {line_number}] Uninitialized variable: {possible_data[0]} ')

    if match_label:
        # * save the labels so when called we can identify them!
        labels.append(possible_lbl.replace(":", ""))
        if possible_lbl == 'DATA:':
            data = True
        elif possible_lbl == 'CODE:':
            data = False
memory_file.close()
# * reset the pointer to read a file from the very beginning after it has been readed once already
instructions_file.seek(0)
# * reset the line counter
line_number = 1
if len(labels) == 0:
    code = True
for i in instructions_file:
    if len(i.split()) == 0:
        line_number += 1
        continue
    assembly_instruction = i.split()[0]
    if code:
        operands = ''.join(i.split()[1:])
        pattern_label = re.compile(label)
        match_label = pattern_label.search(i)
        for j in instructions:
            if j == assembly_instruction:  # * if instruction exists
                for k in instructions[j]:
                    operands_pattern = re.compile(k)
                    operands_match = operands_pattern.search(operands)
                    if operands_match:  # * if operands syntax is right
                        pattern_word = re.compile(words)
                        pattern_letter = re.compile(letter)
                        pattern_decimal = re.compile(decimal)
                        pattern_hexadecimal = re.compile(hexadecimal)
                        # * iterate through the operands to see if they exist
                        for op in operands.split(","):
                            match_word = pattern_word.search(op)
                            match_letter = pattern_letter.search(op)
                            match_decimal = pattern_decimal.search(op)
                            match_hexadecimal = pattern_hexadecimal.search(
                                op)
                            possible_var = op.replace(
                                "(", "").replace(")", "")
                            if match_decimal or match_hexadecimal:  # * if the variable its a number then just continue
                                continue
                            elif match_letter or match_word:
                                if possible_var not in labels and possible_var not in variables:
                                    prRed(
                                        f'[Line {line_number}] Syntax error, the variable or label: {possible_var} has not been defined')
                                    break
                        else:
                            prGreen(
                                f'[Line {line_number}] the instruccion: {i.strip()} is right and its opcode is: {instructions[j][k]}')
                            opcodes_file.write(instructions[j][k] + '\n')
                        break
                else:  # * syntax error in operands
                    prRed(
                        f'[Line {line_number}] Syntax error, wrong operands for the instruccion: {assembly_instruction}')
                break
        else:  # * if it not an instruction
            if match_label:  # * if it's a label
                prGreen(
                    f'[Line {line_number}] the label: {i.strip()} is right')  # TODO: see the case: label: instruction A,B
            else:  # * if its nothing
                prRed(
                    f'[Line {line_number}] Syntax error in label or instruction: {assembly_instruction}')

    if assembly_instruction == 'CODE:':
        code = True
    line_number += 1
opcodes_file.close()
instructions_file.close()
