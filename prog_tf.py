'''This program is only the preliminary part of the entire exercise. The purpose of 
this program is to compute a transfer function of the network. The description of
the network is provided by a netlist which has a standard format. From this the 
network is solved by nodal analysis methods. The type of inputs have been restricted
to independent voltage sources only. The user has to select the output s/he wants
and a transfer function will be computed accordingly. 
The user will then have the option of veiwing different control parameters of the 
circuit such as time-domain response, frequency response and so on. 
'''
import gui_input as gui
import matplotlib.pyplot as plt
import numpy as np
from sympy import *
from sympy.matrices import *
from sympy.parsing.sympy_parser import parse_expr

def diagonal(node_number,from_list,to_list,element_list,value_list):

    '''This function calculates the diagonal elements of the conductance matrix of the system
    For diagonal elements the values are the sum of all the conductances of all the elements 
    connected to the node.
    '''
    s=symbols('s')
    cond_ele=0
    count=0
    for x in range(len(from_list)):
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
    return cond_ele


def offdiagonal(node_number_from,node_number_to,from_list,to_list,element_list,value_list):

    '''This function calculates the off-diagonal elements of the conductance matrix of the system.
    For origin and destination nodes i and j the function returns the negative of the conductance 
    of the element connected between i and j.
    '''
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


def set_cond_matrix(cond,origin,dest,ele,val):

    '''This function builds up the conductance matrix of the system. It fills up the diagonal
    elements by calling the function diagonal with the node number. Similarly the off diagonal elements
    of the conductance matrix is computed by calling the offdiagonal function.
    '''
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
    
    
def set_volt_matrix(volt,volt_trans,origin,dest,ele):
    
    '''This function builds the voltage matrix of the system required for nodal analysis. If the positive 
    side of the first voltage source is connected to node i, say, then volt[0][i]=-1. Such a matrix 
    will be appended to the conductance matrix row-wise. A matrix volt_trans is also created which is
    the volt_matrix with 1's replaced by -1's and vice-versa. This matrix volt_trans is appended to the 
    conductance matrix column wise.
    '''
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

    '''Handles exceptions that may arise due to errors in netlist input by user.
    List of exceptions handled are:-
        -Negative value of nodes-ValueError
        -Negative/Zero value of R,L,C-Value Error
        -Zero value of V-Value Error
    If negative value of the voltage source is given the origin and destination nodes of the source
    are reversed for computational simplicity
    '''
    while True:
        error_flag=0
        gui.main()
        or_nodes,des_nodes=gui.from_list,gui.to_list
        type_of_element,value=gui.ele_type,gui.val_list
        if len(type_of_element) < len(value):
            print("You have not entered all identifiers. Re-enter netlist")
            continue
        if sum(n<0 for n in or_nodes)>0 or sum(n<0 for n in des_nodes)>0:
            print('Negative value of node. Re-enter netlist')
            continue
        for ind in range(len(value)):
            if value[ind]<=0 and 'V' not in type_of_element[ind]:
                print("I dont know how to handle non-positive value of "+type_of_element[ind])
                print("Re-enter netlist")
                error_flag=1
                break
            if value[ind]==0:
                print("Zero value of "+type_of_element[ind])
                print("Re-enter netlist")
                error_flag=1
                break
            if value[ind]<0 and 'V' in type_of_element[ind]:
                print("Reversing polarity of voltage source")
                value[ind]=abs(value[ind])
                or_nodes[ind],des_nodes[ind]=des_nodes[ind],or_nodes[ind]
        if error_flag==1:
            continue
        else:
            break
    return or_nodes,des_nodes,type_of_element,value
	
def check_circuit_error(unknowns,tot_mat,rhs):

    '''Handles exceptions that may arise due to errors in the circuit entered by the user.
    If there are two voltage sources in parallel in the circuit there may be two possible cases:
        -They are of the same value-in which case one voltage source is enough
        -They are of different value-which is not possible practically
    Both of the above cases lead to non-invertibility of the main matrix in nodal analysis. Thus
    both of them are handled.
    '''
    global  soln
    soln={}
    error_flag=0
    for x in range(np.shape(unknowns)[0]):
        if 0 in tot_mat.eigenvals().keys():
            print "There is/are an error/unnecessary voltage sources in your circuit"
            error_flag=1
            break
        else:
            soln[unknowns[x,0]]=simplify((tot_mat.inv()*rhs)[x,0])
    if error_flag==1:
        main()

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
        main()
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
    check_circuit_error(unknowns,tot_mat,rhs)    

        
        
if __name__=='__main__':
    main()

