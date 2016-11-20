"""
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

    Parameters:

     - node_number: decides the index of the conductance matrix to be computed

     - from_list: list of all the origin nodes in the netlist

     - to_list: list of all the destination nodes in the netlist

     - element_list: list of identifiers of elements in the circuit

     - value_list: list of values of elements in the circuit

    Returns:

     - Diagonal element of the conductance matrix

    Method: For filling up conductance[i][i] the ith node is considered and
    conductance of all the elements connected to this node is calculated and
    summed up.
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
    """
    Function calculates the offdiagonal elements of the conductance matrix.

    Parameters:

    - node_number_from: Row-index of the conductance matrix to be computed

    - node_number_to: Column-index of the conductance matrix to be computed

    - from_list: of all the origin nodes in the netlist

    - to_list: list of all the destination nodes in the netlist

    - element_list: list of identifiers of elements in the circuit

    - value_list: list of values of elements in the circuit

    Returns:

    - Offdiagonal element of the conductance matrix.

    Method: For filling up conductance[i][j] the negative of the conductance of
    the element/s connected between i and j the nodes are added up.
    """
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
    """
    Function builds up the conductance matrix of the system.

    Parameters:

    - origin: list of all origin nodes of the netlist

    - dest: list of all destination nodes of the netlist

    - ele: list of all element identifiers of the netlist

    - val: list of values of all the elements in the netlist

    Returns:

    - Conductance matrix of the circuit

    - Number of nodes in the circuit

    """
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
    """
    Function builds the voltage matrix required for nodal analysis.

    Parameters:

    - origin: list of all origin nodes of the netlist

    - dest: list of all destination nodes of the netlist

    - ele: list of all element identifiers of the netlist

    Returns:

    - voltage matrix of the circuit appended to conductance matrix row-wise

    - voltage_trans matrix to be appended to conductance matrix column wise

    - A square matrix of zeros with size equal to number of Voltage sources

    Method:

    If positive end of ith voltage source is connected to a node j, then
    **voltage[i][j]** = 1 and **voltage_trans[i][j]** = -1

    If there are 2 voltage sources the **dep** is a (2 by 2) matrix of 0's
    """
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
    """
    Function calculates the output transfer function as demanded by the user.

    Parameters:

    - solution: dictionary containing solutions of the circuit unknowns

    - o: list containing the originating nodes in the circuit

    - d: list containing the terminating nodes in the circuit

    - e_v: list containing the values of elements in the circuit

    - e_t: list containing the type of elements in the circuit

    - ident: identifier of the required element whose output parameter is asked

    - output_var: I if current is demanded, else V

    Returns:

    - voltage difference across element or current through element

    Method: Calculates the voltage difference between the two nodes between
    which the element of interest is connected. Also calculates the current
    through this element according to the element type.
    """
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
    """
    Function calculates the transfer function as demanded by the user.

    Parameters:

    - sol: dictionary containing solutions of the circuit unknowns

    - or_list: list containing the originating nodes in the circuit

    - des_list: list containing the terminating nodes in the circuit

    - element_value: list containing the values of elements in the circuit

    - element_type: list containing the type of elements in the circuit

    - voltage_sources_num: number of voltage sources in the circuit

    Calls Options method of module gui_control for displaying time response,
    bode, nyquist plot for the computed transfer function.

    Method:

    - Calculates the input as selected by the user

    - Calculates the output transfer function by calling output_tf_calc

    - Calculates coefficients of the resulting transfer function

    - calls the methods of inbuilt control module of Python

    """
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
    """
    Create the matrices required for nodal analysis of the system.

    Parameters:

    - cond: conductance matrix for the system

    - v: voltage matrix of the system

    - val: list of element values of the system

    - v_t: voltage_trans matrix for the system

    - n_nodes: number of nodes for the system

    - n_voltsrc: number of voltage sources for the system

    - ele_type: list of element types of the netlist

    - dep_sources: matrix of zeros for dependent sources

    Nodal analysis involves solving some linear equations given in matrix
    representation as Ax=b

    Returns:

    - unknowns: Matrix of the unknown node voltages and source current

    - tot_mat: Matrix developed from the cond, v,v_t and dep_sources

    - rhs: Matrix prepared from the current through each node and voltage source

    Method:

    if there are 4 nodes in the circuit and one voltage source in the circuit
    then unknowns = transpose([V_1, V_2, V_3, I_V1])

    tot_mat is prepared in the following way

    v appended to cond row-wise
    v_t appended to cond column-wise
    dep_sources appended to make the resulting matrix square

    rhs[i][0] stores the current though node i if i<=n_nodes
    rhs[j][0] stores the value of the voltage source  numbered j-(n_nodes)
    """
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
    """
    Solve the nodal analysis equations.

    Nodal analysis equation: Ax=b

    Parameters:

    - unknowns: x in the nodal analysis equations

    - tot_mat: A in the nodal analysis equations

    - rhs: b in the nodal analysis equations

    Returns:

    - soln: solution of the nodal analysis equations

    Method:

    If there are unnecessary voltage sources in the circuit the matrix A is not
    invertible. Such errors are handled in this function.
    x is calculated if A is invertible as inv(A)*b
    If A is not invertible thereby signifying circuit error user is given the
    option of re-entering circuit netlist.
    """
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
    """
    Input accepted from user for netlist.

    If there is an error in the circuit entered by user, user is asked whether
    s/he wants to re-enter.

    After a proper circuit is entered by user, the circuit is solved by calling
    function **check_circuit_error**.

    transfer function is then computed in the function
    **input_output_calculation**.
    """
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
