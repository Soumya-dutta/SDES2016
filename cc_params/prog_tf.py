"""This program is only the preliminary part of the entire exercise.

The purpose of this program is to compute a transfer function of the network.
The description of the network is provided by a netlist which has a standard
format. From this the network is solved by nodal analysis methods. The type of
inputs have been restricted to independent voltage sources only. The user has
to select the output s/he wants and a transfer function will be computed
accordingly. The user will then have the option of veiwing different control
parameters of the circuit such as time-domain response, frequency response and
so on.
"""

import gui_input as gui
import gui_tf_io as gui_io
import gui_control as control
import numpy as np
from sympy import symbols, simplify, Poly
from sympy.matrices import Matrix
from sympy.parsing.sympy_parser import parse_expr


def diagonal(node_number, from_list, to_list, element_list, value_list):
    """
    Function calculates the diagonal elements of the conductance matrix.

    For diagonal elements the values are the sum of all the conductances of all
    the elements connected to the node.
    """
    s = symbols('s')
    cond_ele = 0
    for x in range(len(from_list)):
        if 'V' in element_list[x]:
            continue
        elif ('R' in element_list[x] and
                (from_list[x] == node_number or to_list[x] == node_number)):
            cond_ele = cond_ele+float(1/value_list[x])
        elif ('L' in element_list[x] and
                (from_list[x] == node_number or to_list[x] == node_number)):
            cond_ele = cond_ele+float(1/value_list[x])/s
        elif ('C' in element_list[x] and
                (from_list[x] == node_number or to_list[x] == node_number)):
            cond_ele = cond_ele+float(value_list[x])*s
    return cond_ele


def offdiagonal(node_number_from, node_number_to, from_list, to_list,
                element_list, value_list):

    '''This function calculates the off-diagonal elements of the conductance
     matrix of the system.For origin and destination nodes i and j the function
     returns the negative of the conductance of the element connected
     between i and j.
    '''
    s = symbols('s')
    cond_ele = 0
    for x in range(len(from_list)):
        if 'V' in element_list[x]:
            continue
        elif 'R' in element_list[x] and (from_list[x] == node_number_from and
                                         to_list[x] == node_number_to):
            cond_ele = cond_ele+float(-1/value_list[x])
        elif 'L' in element_list[x] and (from_list[x] == node_number_from and
                                         to_list[x] == node_number_to):
            cond_ele = cond_ele+float(-1/value_list[x])/s
        elif 'C' in element_list[x] and (from_list[x] == node_number_from and
                                         to_list[x] == node_number_to):
            cond_ele = cond_ele+float(-1*value_list[x])*s
    return cond_ele


def set_cond_matrix(origin, dest, ele, val):

    '''This function builds up the conductance matrix of the system. It fills up
     the diagonal elements by calling the function diagonal with the
     node number. Similarly the off diagonal elements of the conductance matrix
     is computed by calling the offdiagonal function.
    '''
    num_nodes = max(max(origin), max(dest))
    cond = Matrix.zeros(num_nodes, num_nodes)
    (row, col) = np.shape(cond)
    for row_ind in range(row):
        for col_ind in range(row_ind, col):
            if row_ind == col_ind:
                diag_ele = diagonal(row_ind+1, origin, dest, ele, val)
                cond[row_ind, col_ind] = parse_expr(str(diag_ele))
            else:
                off_diag_ele = offdiagonal(row_ind+1, col_ind+1, origin, dest,
                                           ele, val)
                cond[row_ind, col_ind] = parse_expr(str(off_diag_ele))
                cond[col_ind, row_ind] = parse_expr(str(off_diag_ele))
    return cond, num_nodes


def set_volt_matrix(origin, dest, ele):

    '''This function builds the voltage matrix of the system required for nodal
    analysis. If the positive side of the first voltage source is connected to
    node i, say, then volt[0][i]=-1. Such a matrix will be appended to the
    conductance matrix row-wise. A matrix volt_trans is also created which is
    the volt_matrix with 1's replaced by -1's and vice-versa. This matrix
    volt_trans is appended to the conductance matrix column wise.
    '''
    num_nodes = max(max(origin), max(dest))
    number_of_voltage_sources = len([1 for x in ele if 'V' in x])
    voltage = Matrix.zeros(num_nodes, number_of_voltage_sources)
    voltage_trans = Matrix.zeros(number_of_voltage_sources, num_nodes)
    (row, col) = np.shape(voltage)
    for row_ind in range(row):
        for col_ind in range(col):
            for x in range(len(origin)):
                if ele[x] == "V"+str(col_ind+1) and origin[x] == row_ind+1:
                    voltage[row_ind, col_ind] = -1
                    voltage_trans[col_ind, row_ind] = 1
                elif ele[x] == "V"+str(col_ind+1) and dest[x] == row_ind+1:
                    voltage[row_ind, col_ind] = 1
                    voltage_trans[col_ind, row_ind] = -1
    dep = Matrix.zeros(number_of_voltage_sources, number_of_voltage_sources)
    return voltage, voltage_trans, dep


def output_tf_calc(solution, o, d, e_v, e_t, ident, output_var):

    '''This function takes the following arguments:
    solution- dictionary containing solutions of the circuit unknowns
    o- list containing the originating nodes in the circuit
    d- list containing the terminating nodes in the circuit
    e_v- list containing the element values of the circuit
    e_t- list containing all the identifiers of the circuit elements
    ident- identifier of the required element whose output parameter is sought
    output_var- tells whether user demands current(I) or voltage(V)

    Depending on the value of the originating and ending node of the identifier
    required volt_diff is calculated. Further depending on the type of ident
    that is R,L,C,V the current throught the element is calculated.

    If output_var = "V", the volt_diff is returned
    If output_var = "I", the variable current is returned.
    '''
    s = symbols('s')
    ind = e_t.index(ident)
    origin_node, ending_node, value_of_element = o[ind], d[ind], e_v[ind]
    if origin_node != 0 and ending_node == 0:
        volt_diff = solution[parse_expr("V_"+str(origin_node))]-parse_expr("0")
    elif origin_node == 0 and ending_node != 0:
        volt_diff = parse_expr("0")-solution[parse_expr("V_"+str(ending_node))]
    else:
        volt_diff = solution[parse_expr("V_"+str(origin_node))]-solution[
                                       parse_expr("V_"+str(ending_node))]
    if 'R' in ident:
        current = volt_diff/value_of_element
    elif 'L' in ident:
        current = volt_diff/((value_of_element)*s)
    elif 'C' in ident:
        current = volt_diff*value_of_element*s
    else:
        current = solution[parse_expr("I_"+ident)]

    if output_var == 'V':
        return volt_diff
    else:
        return current


def input_output_calculation(sol, or_list, des_list, element_type,
                             element_value, voltage_sources_num):

    '''This functions interfaces the gui functionality provided by gui_tf_io.py
    with this program. Once the netlist entered by the user passes all the
    checks the user has to select the input and output of the transfer function
    Input value is directly received by this function from gui_tf_io.py
    Output value has to be calculated. gui_tf_io.py creates two variables
    for sending the output demanded.

    For eg: if current through element L1 in any circuit is demanded,
    output_type variable is set to I
    ele_identifier is set to L1.

    This information is used by the called function output_tf_calc
    '''
    s = symbols('s')
    gui_tf_input_calc = gui_io.Input_selection(element_type, element_value,
                                               voltage_sources_num)
    gui_tf_output = gui_io.Output_selection(element_type)
    tf_numerator = output_tf_calc(sol, or_list, des_list, element_value,
                                  element_type, gui_tf_output.ele_identifier,
                                  gui_tf_output.output_type)
    tf_denominator = simplify(gui_tf_input_calc.inpval)
    inp_out_tf = simplify(tf_numerator/tf_denominator)
    num, den = inp_out_tf.as_numer_denom()
    num_coeffs = list(Poly(num, s).all_coeffs())
    den_coeffs = list(Poly(den, s).all_coeffs())
    num_coeffs = [round(a, 10) for a in num_coeffs]
    den_coeffs = [round(a, 10) for a in den_coeffs]
    control.Options(num_coeffs, den_coeffs)


def nodal_matrix(cond, v, val, v_t, n_nodes, n_voltsrc, ele_type, dep_sources):
    tot_mat_upper = cond.row_join(v)
    tot_mat_down = v_t.row_join(dep_sources)
    tot_mat = tot_mat_upper.col_join(tot_mat_down)
    node_voltage = Matrix.zeros(n_nodes, 1)
    current_voltage = Matrix.zeros(n_voltsrc, 1)
    for n in range(1, n_nodes+1):
        node_voltage[n-1, 0] = symbols('V_'+str(n))
    for n in range(1, n_voltsrc+1):
        current_voltage[n-1, 0] = symbols('I_V'+str(n))
    unknowns = node_voltage.col_join(current_voltage)
    current_node = Matrix.zeros(n_nodes, 1)
    voltage_source = Matrix.zeros(n_voltsrc, 1)
    for x in range(n_voltsrc):
        ind = list(ele_type).index("V"+str(x+1))
        voltage_source[x, 0] = val[ind]
    rhs = current_node.col_join(voltage_source)
    return unknowns, tot_mat, rhs


def check_circuit_error(unknowns, tot_mat, rhs):

    '''Handles exceptions that may arise due to errors in the circuit entered
     by the user.If there are two voltage sources in parallel in the circuit
     there may be two possible cases:
        -They are of the same value-in which case one voltage source is enough
        -They are of different value-which is not possible practically
    Both of the above cases lead to non-invertibility of the main matrix in
    nodal analysis. Thus both of them are handled.
    '''
    soln = {}
    error_flag = 0
    for x in range(np.shape(unknowns)[0]):
        if 0 in tot_mat.eigenvals().keys():
            print("Error in circuit")
            error_flag = 1
            break
        else:
            soln[unknowns[x, 0]] = simplify((tot_mat.inv()*rhs)[x, 0])
    if error_flag == 1:
        main()
    else:
        return soln


def main():

    continue_flag = 0
    gui_inputs = gui.Input_screen()
    if gui_inputs.error_flag == 1:
        gui_input_error = gui.Error(gui_inputs.error_msg)
        if gui_input_error.decision == "Yes":
            main()
    else:
        or_nodes = gui_inputs.origin_list
        des_nodes = gui_inputs.destination_list
        type_of_element, value = gui_inputs.ele_type, gui_inputs.val_list
        continue_flag = 1
    if continue_flag == 1:
        conductance, num_nodes = set_cond_matrix(or_nodes, des_nodes,
                                                 type_of_element, value)
        voltage, voltage_trans, dep = set_volt_matrix(or_nodes, des_nodes,
                                                      type_of_element)
        number_of_voltage_sources = dep.shape[1]
        unknowns, tot_mat, rhs = nodal_matrix(conductance, voltage, value,
                                              voltage_trans, num_nodes,
                                              number_of_voltage_sources,
                                              type_of_element, dep)
        soln = check_circuit_error(unknowns, tot_mat, rhs)
        input_output_calculation(soln, or_nodes, des_nodes, type_of_element,
                                 value, number_of_voltage_sources)


if __name__ == '__main__':
    main()
