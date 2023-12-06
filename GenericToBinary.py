# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:50:48 2020

@author: kalai
"""
import re

def write_to_text_file(filename,f_string):
	with open(filename,'a') as afile:
		afile.write(f_string)

def convert_to_binary(file):
    w_j = []
    count_w = 1
    f = open(file,'r')
    filelines = f.readlines()
    MinMax,function = minmax(filelines[0]),binary_function(filelines[1:-1])
    ineq_operators = binary_constraints_operators(filelines[-1],filelines[0][0:3])
    constraints,coefficients,operators_lists = [],[],[]
    index = 0
    j = 1
    binary_constraints_coef,binary_constraints_oper = [],[]

    constraints_count = len(filelines)-2
    
    largest_var = get_largest_var(filelines[-1]) 
    
    right_side,right_operators = binary_right_side(filelines[0],largest_var)
            
    #Constraints of binary problem
    for line in filelines[1:-1]:
        coefficients_line,operators_line = get_coefficients(line,constraints_count,largest_var)
        coefficients.append(coefficients_line)
        operators_lists.append(operators_line)
        
    binary_constraints_coef = get_correct_order(coefficients)
    binary_constraints_oper = get_correct_order(operators_lists)
    
    for line in range(largest_var):
        constrain = ''
        oper_index = 0
        for i in binary_constraints_coef[index]:
            if i != 0:
                if i != 1:
                    constrain += binary_constraints_oper[index][oper_index] + ' ' + str(i) + 'w' + str(j) + ' '
                else:
                    constrain += binary_constraints_oper[index][oper_index] + ' ' + 'w' + str(j) + ' '
            oper_index += 1
            j += 1
        j=1

        if constrain[0] == '+':
            constrain = constrain[1:]
            
        constrain += ineq_operators[index] + ' '
        if right_operators[index] == '-':
            constrain += right_operators[index] + str(right_side[index])
        else:
            constrain += str(right_side[index])
        constraints.append(constrain)
        index += 1
        
    #Last line of binary problem
    for line in filelines[1:-1]:
        w_j.append('w' + str(count_w) + ' ' + binary_var_constraints(line,filelines[0][0:3]))
        count_w += 1
    
    
    return function,constraints,w_j,MinMax

    
def get_correct_order(alist):
    index = 0
    tmp_list,correct_order_list = [],[]
    
    for i in range(len(alist[0])):
        for x in alist:
            tmp_list.append(x[index])
        correct_order_list.append(tmp_list)
        tmp_list = []
        index += 1
        
    return correct_order_list
            

def minmax(firstline):
    line_seperated = firstline.split()
    if line_seperated[0] == 'max':
        return 'min'
    elif line_seperated[0] == 'min':
        return 'max'
    
def binary_function(lines): 
    function = []
    var_count = 1
    index = 0
    
    for i in lines:
        line_seperated = lines[index].split()            
            
        if '-' in line_seperated[-2]:
            function.append('-' + ' ')
        else:
            if index != 0:
                function.append('+' + ' ')
                    
        if line_seperated[-1] != '0':
            function.append(line_seperated[-1])
            function.append('w'+str(var_count) + ' ')
        var_count += 1
        index += 1
        
    function = ''.join(function)

    return function

def binary_var_constraints(line,minmax):
    line_seperated = line.split()
    if minmax == 'min':
        if '-' not in line_seperated[-2]:
            if '>=' in line_seperated[-2]:
                return '>= 0'
            elif '<=' in line_seperated[-2]:
                return '<= 0'
            else:
                return 'free'
        else:
            if '>=' in line_seperated[-3]:
                return '>= 0'
            elif '<=' in line_seperated[-3]:
                return '<= 0'
            else:
                return 'free'
    else:
        if '-' not in line_seperated[-2]:
            if '>=' in line_seperated[-2]:
                return '<= 0'
            elif '<=' in line_seperated[-2]:
                return '>= 0'
            else:
                return 'free'
        else:
            if '>=' in line_seperated[-3]:
                return '<= 0'
            elif '<=' in line_seperated[-3]:
                return '>= 0'
            else:
                return 'free'
              
def get_largest_var(line):
    
    x_j = re.findall('\d',line)
    x_j.remove('0')
    x_j = [int(x) for x in x_j ]
    var_count = x_j[-1]
    
    return var_count


def binary_constraints_operators(line,minmax):
    
    x_j = re.findall('\d',line)
    x_j.remove('0')
    x_j = [int(x) for x in x_j ]
    var_count = x_j[-1]
    
    res = [ele for ele in range(var_count) if ele not in x_j] 
    res.remove(0)
    
    constraints_operators = []
    
    for i in range(x_j[-1]):
        if minmax == 'min':
            constraints_operators.append('<=')
        else:
            constraints_operators.append('>=')
    
    for i in res:
        constraints_operators[i-1] = '='

        
    return constraints_operators
    
            
def get_coefficients(line,constraints_count,largest_var):
     
    line_seperated = line.split()
    line_seperated.pop()
    line_seperated.pop()
    line = ' '.join(line_seperated)
    
    operators = re.findall('[+-]',line)
    
    vars_index = re.findall('x\d',line)
    vars_index = [s.strip('x') for s in vars_index]
    vars_index = [int(x) for x in vars_index ]
    
    if len(operators) != len(vars_index):
        operators.insert(0,'+')
    
    vars_coefficient_equal_to_one = re.findall('[^\dx]x\d',line)
    vars_coefficient_equal_to_one = [s.strip() for s in vars_coefficient_equal_to_one]
    vars_coefficient_equal_to_one = [s.strip('x') for s in vars_coefficient_equal_to_one]
    vars_coefficient_equal_to_one = [int(x) for x in vars_coefficient_equal_to_one]

    coefficients = re.findall('\dx',line)
    coefficients = [s.strip('x') for s in coefficients]
    coefficients = [int(x) for x in coefficients]
    
    if line[0] == 'x':
        vars_coefficient_equal_to_one.insert(0,1)
    
    res = [ele for ele in range(constraints_count) if ele not in vars_index]
    if 0 in res:
        res.remove(0)
            
    for i in res:
       coefficients.insert(i-1,0)

    for i in vars_coefficient_equal_to_one:
        coefficients.insert(i-1,1)
           
    if len(coefficients) > len(operators):
        for i in res:
            operators.insert(i-1,'')
            
    while len(coefficients) < largest_var:
        coefficients.append(0)
        
    while len(operators) < largest_var:
        operators.append('')
    
            
    return coefficients,operators
    
def binary_right_side(firstline,largest_var):
    
    operators = re.findall('[+-]',firstline)
    
    varsx_indexes = re.findall('x\d',firstline)
    varsx_indexes = [s.strip('x') for s in varsx_indexes]
    varsx_indexes = [int(x) for x in varsx_indexes ]  
    
    vars_coefficient_equal_to_one = re.findall('[^\dx]x\d',firstline)
    vars_coefficient_equal_to_one = [s.strip() for s in vars_coefficient_equal_to_one]
    vars_coefficient_equal_to_one = [s.strip('x') for s in vars_coefficient_equal_to_one]
    vars_coefficient_equal_to_one = [int(x) for x in vars_coefficient_equal_to_one]
    
    if firstline[0] == 'x':
        vars_coefficient_equal_to_one.insert(0,1)

    res = [ele for ele in range(largest_var) if ele not in varsx_indexes] 
    if 0 in res:
        res.remove(0)
        
    if len(varsx_indexes) != len(operators):
        operators.insert(0,'+')
        
    x_coefficients = re.findall('\dx',firstline)
    x_coefficients = [s.strip('x') for s in x_coefficients]
    x_coefficients = [int(x) for x in x_coefficients ]
    
    for i in res:
        x_coefficients.insert(i-1,0)
        
    for i in vars_coefficient_equal_to_one:
        x_coefficients.insert(i-1,1)
        
    for i in range(largest_var):
        if len(x_coefficients) != largest_var:
            x_coefficients.append(0)
    
    for i in range(largest_var):        
        if len(x_coefficients) != len(operators):
            operators.append('')
    
    return x_coefficients,operators



function,constraints,w_j,MinMax = convert_to_binary('lp1.txt')
write_to_text_file('lp2.txt',f'{MinMax} {function}\n')
for i in range(len(constraints)):
    if i==0:
        write_to_text_file('lp2.txt',f's.t. {constraints[i]}\n')
    else:
        write_to_text_file('lp2.txt',f'\t {constraints[i]}\n')
for i in range(len(w_j)):
    write_to_text_file('lp2.txt',f'{w_j[i]}')
    if i != len(w_j)-1:
        write_to_text_file('lp2.txt',', ')
    
    



    
    
    
    
        
        
        
    

    
