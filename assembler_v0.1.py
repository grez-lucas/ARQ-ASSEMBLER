instrucciones={"MOV":[["A","B"],["B","A"],["A","Lit"],["B","Lit"],["A","(Dir)"],["B","(Dir)"],["(Dir)","A"],["(Dir)","B"],["A","(B)"],["B","(B)"],["(B)","A"]],
     "ADD":[["A","B"],["B","A"],["A","Lit"],["B","Lit"],["A","(Dir)"],["B","(Dir)"], ["A","(B)"], ["(Dir)"]],
     "SUB":[["A","B"],["B","A"],["A","Lit"],["B","Lit"],["A","(Dir)"],["B","(Dir)"],["A","(B)"],["(Dir)"]],
     "AND":[["A","B"],["B","A"],["A","Lit"],["B","Lit"],["A","(Dir)"],["B","(Dir)"], ["A","(B)"], ["(Dir)"]],
     "OR":[["A","B"],["B","A"],["A","Lit"],["B","Lit"],["A","(Dir)"],["B","(Dir)"],["A","(B)"],["(Dir)"]],
     "NOT":[["A","A"],["A","B"],["B","A"],["B","B"],["(Dir)","A"],["(Dir)","B"],["(B)"]],
     "XOR":[["A","B"],["B","A"],["A","Lit"],["B","Lit"],["A","(Dir)"],["B","(Dir)"],["A","(B)"],["(Dir)"]],
     "SHL":[["A","A"],["A","B"],["B","A"],["B","B"],["(Dir)","A"],["(Dir)","B"],["(B)"]],
     "SHR":[["A","A"],["A","B"],["B","A"],["B","B"],["(Dir)","A"],["(Dir)","B"],["(B)"]],
     "INC":[["B"],["(Dir)"],["(B)"]],
     "RST":[["(Dir)"],["(B)"]],
     "CMP":[["A","B"],["A","Lit"],["B","Lit"],["A","(Dir)"],["B","(Dir)"],["A","(B)"]],
     "JMP":[["Dir"]],
     "JEQ":[["Dir"]],
     "JNE":[["Dir"]],
     "JGT":[["Dir"]],
     "JLT":[["Dir"]],
     "JGE":[["Dir"]],
     "JLE":[["Dir"]],
     "JCR":[["Dir"]],
     "JOV":[["Dir"]],
     "CALL":[["Dir"]],
     "RET": [[]], #en las instrucciones aparece vacio
     "PUSH": [["A"],["B"]],
     "POP" : [["A","B"]]
     }

def ver_num(numero):

    aux=numero

    if (numero[0]=="(" and numero[-1]==")"):
        aux=numero[1:-1]

    if (aux[0]=="#"):
        aux=aux[1:]
        try:
            aux=int(aux,16) #hexadecimal
        except:
            print("no es numero")
            return False
    else:
        try:
            aux=int(aux) #transformacion directa
        except:
            print("no es numero")
            return False
            
    if (aux not in range(0,255)): #maximo 250
        print("fuera de rango")
        return False
    return True
    
def ver_op(operadores,valid_num):
    op_final=[]
    cantidad = len(operadores)
   
    if cantidad==1: #1 operador
        if operadores[0]!="A" and operadores[0]!="B":
            if valid_num:
                valid_num=ver_num(operadores[0])
            if ("B" not in operadores) and operadores[0][0]=="("and operadores[0][-1]==")" :
                ver_num
                op_final.append("(Dir)")
            else:
                op_final.append("Dir")
        else:
             op_final= operadores
                
    elif cantidad==2: #2 operadoresS
        if operadores[0]!="B" and operadores[0]!="(B)" and operadores[0]!="A":
            if valid_num:
                valid_num=ver_num(operadores[0]) #verifica si es valido el numero
            if operadores[0][0]=="("and operadores[0][-1]==")" and ("B" not in operadores[0]):
                op_final.append("(Dir)")
                op_final.append(operadores[1])
            else:
                op_final.append("Lit")
                op_final.append(operadores[1])
        elif operadores[1]!="B" and operadores[1]!="(B)" and operadores[1]!="A":
            if valid_num:
                valid_num=ver_num(operadores[1])
            if operadores[1][0]=="(" and operadores[1][-1]==")" and ("B" not in operadores[0]):      
                op_final.append(operadores[0])
                op_final.append("(Dir)")
            
            else:
                op_final.append(operadores[0])
                op_final.append("Lit")
        else:
            op_final = operadores ##si no, se mantiene
    return op_final, valid_num


    
def ver(instruccion):
    valid_num=True #bool para verificar (si es numero), la operacion
    op_nueva, booleano =ver_op(instruccion[1],valid_num) #verificamos la operacion 
    if instruccion[0] not in instrucciones.keys():
        return 1

    elif op_nueva not in instrucciones[instruccion[0]] and booleano:
        return 2


def imprimir(cont,pivote,instruccion): #se imprime el tipo de error con la linea de codigo correspondiente
    if ver(instruccion) == 1:
        print("error: La instruccion de la linea " +str(cont)+ " es incorrecta")
        print("linea "+str(cont)+": " +str(pivote))
        
    elif ver(instruccion) == 2:
        print("error: La operacion de la linea " +str(cont)+ " es incorrecta")
        print("linea "+str(cont)+": " +str(pivote))
        
        
        



archivo = open("incorrecto.ass", "r")


cont = 1
inc = 0
for linea in archivo.readlines():
    pivote= linea.strip()# se usa solo para imprimir la linea de error

    x=linea.strip().split(" ")
    operacion=x[1].split(",")
    instruccion=[x[0],operacion] #tipo [string,arreglo de operaciones]
    ver(instruccion) #verificar
    imprimir(cont,pivote,instruccion)
    cont += 1   



archivo.close()