'''
This program is only the preliminary part of the entire exercise. The purpose of 
this program is to compute a transfer function of the network. The description of
the network is provided by a netlist which has a standard format. From this the 
network is solved by nodal analysis methods. The type of inputs have been restricted
to independent voltage sources only. The user has to select the output s/he wants
and a transfer function will be computed accordingly. 
The user will then have the option of veiwing different control parameters of the 
circuit such as time-domain response, frequency response and so on. 
'''

import matplotlib.pyplot as plt
import control
import math
import string
import pandas as pd
import numpy as np
from scipy import signal
from sympy import *
from sympy.matrices import *
from sympy.parsing.sympy_parser import parse_expr

#This function calculates the diagonal elements of the conductance matrix of the system 

def diagonal(node_number,from_list,to_list,element_list,value_list):


    s=symbols('s')
    cond_ele=0
    count=0
    for x in range(len(from_list)):
        if 'V' in element_list[x]:
            continue
        elif 'R' in element_list[x] and (from_list[x]==node_number or to_list[x]==node_number):
            cond_ele=cond_ele+float(1/value_list[x])
        elif 'L' in element_list[x] and (from_list[x]==node_number or to_list[x]==node_number):
            cond_ele=cond_ele+float(1/value_list[x])/s
        elif 'C' in element_list[x] and (from_list[x]==node_number or to_list[x]==node_number):
            cond_ele=cond_ele+float(value_list[x])*s
    return cond_ele

#This function calculates the off-diagonal elements of the conductance matrix of the system 

def offdiagonal(node_number_from,node_number_to,from_list,to_list,element_list,value_list):
    s=symbols('s')
    cond_ele=0
    for x in range(len(from_list)):
        if 'V' in element_list[x]:
            continue
        elif 'R' in element_list[x] and (from_list[x]==node_number_from and to_list[x]==node_number_to):
            cond_ele=cond_ele+float(-1/value_list[x])
        elif 'L' in element_list[x] and (from_list[x]==node_number_from and to_list[x]==node_number_to):
            cond_ele=cond_ele+float(-1/value_list[x])/s
        elif 'C' in element_list[x] and (from_list[x]==node_number_from and to_list[x]==node_number_to):
            cond_ele=cond_ele+float(-1*value_list[x])*s
    return cond_ele

#This function builds up the conductance matrix of the system 

def set_cond_matrix(cond,origin,dest,ele,val):
    (row,col)=np.shape(cond)
    for row_ind in range(row):
        for col_ind in range(row_ind,col):
            if row_ind==col_ind:
                diag_ele=diagonal(row_ind+1,origin,dest,ele,val)
                cond[row_ind,col_ind]=parse_expr(str(diag_ele))
            else:
                off_diag_ele=offdiagonal(row_ind+1,col_ind+1,origin,dest,ele,val)
                cond[row_ind,col_ind]=parse_expr(str(off_diag_ele))
                cond[col_ind,row_ind]=parse_expr(str(off_diag_ele))
    return cond

    
def main():
    s=symbols('s')
    net_list=pd.read_csv('netlist.csv')
    or_nodes,des_nodes,type_of_element,value=net_list['From'],net_list['To'],net_list['Type'],net_list['Value']
    num_nodes=max(max(or_nodes),max(des_nodes))
    conductance=Matrix.zeros(num_nodes,num_nodes)
    conductance=set_cond_matrix(conductance,or_nodes,des_nodes,type_of_element,value)
        
if __name__=='__main__':
    main()

