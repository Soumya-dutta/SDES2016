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
    try:
        for x in range(len(from_list)):
            type_pass_ele=element_list[x][0]
            if 'V' in element_list[x]:
                continue
            elif ('R' in element_list[x] 
                        and (from_list[x]==node_number or to_list[x]==node_number)):
                cond_ele=cond_ele+float(1/value_list[x])
            elif ('L' in element_list[x] and 
                        (from_list[x]==node_number or to_list[x]==node_number)):
                cond_ele=cond_ele+float(1/value_list[x])/s
            elif ('C' in element_list[x] and 
                        (from_list[x]==node_number or to_list[x]==node_number)):
                cond_ele=cond_ele+float(value_list[x])*s
            elif (type_pass_ele!='R' and type_pass_ele!='C' and
                                        type_pass_ele!='V' and type_pass_ele!='L'):
                print(element_list[x]+" is not recognized")
                raise AttributeError('Unrecognized passive element')
    except AttributeError:
        print("Check your netlist. You have entered an unknown passive element")
        print("You can enter R,L,C or V")
        raise
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
    
#This function builds the voltage matrix of the system required for nodal analysis
    
def set_volt_matrix(volt,volt_trans,origin,dest,ele):
    (row,col)=np.shape(volt)
    for row_ind in range(row):
        for col_ind in range(col):
            for x in range(len(origin)):
                if ele[x]=="V"+str(col_ind+1) and origin[x]==row_ind+1:
                    volt[row_ind,col_ind]=-1
                    volt_trans[col_ind,row_ind]=1
                elif ele[x]=="V"+str(col_ind+1) and dest[x]==row_ind+1:
                    volt[row_ind,col_ind]=1
                    volt_trans[col_ind,row_ind]=-1
    return volt,volt_trans

def check_netlist_error():

    try:
        net_list=pd.read_csv('netlist.csv')
        or_nodes,des_nodes=net_list['From'],net_list['To']
        type_of_element,value=[x.upper() for x in net_list['Type']],net_list['Value']
        type_or,type_des=[type(x) for x in or_nodes],[type(x) for x in des_nodes]
        type_value = [type(x) for x in value]
        if len(set(type_of_element)) != len(type_of_element):
            print("You have entered same identifier more than once")
            raise NameError
        if str in type_or or str in type_des or str in type_value:
            raise TypeError('String encountered')
        if sum(n<0 for n in or_nodes)>0 or sum(n<0 for n in des_nodes)>0:
            raise ValueError('Negative value of node')
    except TypeError:
        print("You entered a string when you where supposed to enter a number")
        raise
    except ValueError:
        print("You have entered a negative value of node")
        raise
    for ind in range(len(value)):
        if value[ind]<=0 and 'V' not in type_of_element[ind]:
            print("I dont know how to handle non-positive value of "+type_of_element[ind])
            raise ValueError
        if value[ind]==0:
            print("Zero value")
            raise ValueError
        if value[ind]<0 and 'V' in type_of_element[ind]:
            print("Reversing polarity of voltage source")
            value[ind]=abs(value[ind])
            or_nodes[ind],des_nodes[ind]=des_nodes[ind],or_nodes[ind]
    return or_nodes,des_nodes,type_of_element,value
	
def check_circuit_error(unknowns,tot_mat,rhs):

    soln={}
    for x in range(np.shape(unknowns)[0]):
        try:
            if tot_mat.det==0:
                raise ValueError
            else:
                soln[unknowns[x,0]]=simplify((tot_mat.inv()*rhs)[x,0])
        except ValueError:
            print "There is an error/unnecessary voltage sources in your circuit"
            raise 
    return soln


def main():

    s=symbols('s')
    or_nodes,des_nodes,type_of_element,value=check_netlist_error()  
    num_nodes=max(max(or_nodes),max(des_nodes))
    conductance=Matrix.zeros(num_nodes,num_nodes)
    conductance=set_cond_matrix(conductance,or_nodes,des_nodes,
                                type_of_element,value)
    number_of_voltage_sources=len([1 for x in type_of_element if 'V' in x])
    if number_of_voltage_sources==0:
        print("You have forgotten to enter your source. Please re-enter")
        raise AttributeError
    voltage=Matrix.zeros(num_nodes,number_of_voltage_sources)
    voltage_trans=Matrix.zeros(number_of_voltage_sources,num_nodes)
    voltage,voltage_trans=set_volt_matrix(voltage,voltage_trans,or_nodes,
                                            des_nodes,type_of_element)
    dep=Matrix.zeros(number_of_voltage_sources,number_of_voltage_sources)
    tot_mat_upper=conductance.row_join(voltage)
    tot_mat_down=voltage_trans.row_join(dep)
    tot_mat=tot_mat_upper.col_join(tot_mat_down)
    node_voltage=Matrix.zeros(num_nodes,1)
    current_voltage=Matrix.zeros(number_of_voltage_sources,1)
    for n in range(1,num_nodes+1):
        node_voltage[n-1,0]=symbols('V_'+str(n))
    for n in range(1,number_of_voltage_sources+1):
        current_voltage[n-1,0]=symbols('I_V'+str(n))
    unknowns=node_voltage.col_join(current_voltage)
    current_node=Matrix.zeros(num_nodes,1)
    voltage_source=Matrix.zeros(number_of_voltage_sources,1)
    for x in range(number_of_voltage_sources):
        ind=list(type_of_element).index("V"+str(x+1))
        voltage_source[x,0]=value[ind]
    rhs=current_node.col_join(voltage_source)
    soln=check_circuit_error(unknowns,tot_mat,rhs)    

        
        
if __name__=='__main__':
    main()

