"""symbols and Matric are imported from sympy library.

os and sys are used to access the program that is being tested and present
in the cc_params directory.
"""
import os
import sys
from sympy import symbols
from sympy.matrices import Matrix
module_path = os.path.dirname(os.path.pardir + os.path.sep)
module_path = os.path.join(module_path, "cc_params")
sys.path.insert(0, os.path.abspath(module_path))
import prog_tf as prog


def test_conductance_matrix():
    """
    Test the formation of the conductance matrix for 4 given networks.

    Network1: Voltage source is not connected to the ground.
    Network2: A simple series RLC circuit
    Network3: A network with three elements connected between two nodes
    Network4: A complex network with 5 nodes (including the reference node)

    In order to test only specific functions we add attributes to the required
    test functions. The attribute used is will_run.

    To run this test use: nosetests -a will_run test_prog_tf.py
    """
    s = symbols('s')
    o, d = [1, 0, 2, 1], [0, 2, 3, 3]
    e, v = ["R1", "R2", "R3", "V1"], [0.2, 0.2, 0.2, 5]
    test_output = Matrix([[5.0, 0.0, 0.0], [0, 10.0, -5.0], [0.0, -5.0, 5.0]])
    assert(prog.set_cond_matrix(o, d, e, v)) == (test_output, 3)
    o, d = [1, 2, 3, 1], [2, 3, 0, 0]
    e, v = ["R1", "L1", "C1", "V1"], [5.0, 10.0, 1e-6, 5.0]
    test_output = Matrix([[0.2, -0.2, 0.0], [-0.2, 0.2+0.1/s, -0.1/s],
                          [0.0, -0.1/s, 0.1/s+1e-6*s]])
    assert(prog.set_cond_matrix(o, d, e, v)) == (test_output, 3)
    o, d = [1, 2, 3, 3, 3, 1], [2, 3, 0, 0, 0, 0]
    e = ["R1", "C1", "C2", "L1", "R2", "V1"]
    v = [10.0, 1e-6, 1e-6, 10.0, 5.0, 5.0]
    test_output = Matrix([[0.1, -0.1, 0], [-0.1, 0.1+1e-6*s, -1e-6*s],
                          [0, -1e-6*s, 2*s*1e-6+0.1/s+0.2]])
    assert(prog.set_cond_matrix(o, d, e, v)) == (test_output, 3)
    o, d = [1, 2, 2, 3, 3, 4, 1], [2, 3, 0, 0, 4, 0, 0]
    e = ["R1", "R2", "L1", "C1", "R3", "R4", "V1"]
    v = [10.0, 10.0, 10.0, 1e-6, 10.0, 10.0, 5.0]
    test_output = Matrix([[0.1, -0.1, 0, 0], [-0.1, 0.2+0.1/s, -0.1, 0],
                          [0, -0.1, 0.2+1e-6*s, -0.1], [0, 0, -0.1, 0.2]])
    assert(prog.set_cond_matrix(o, d, e, v)) == (test_output, 4)


def test_voltage_matrix():
    """
    Test the formation of the volatge matrix required for nodal analysis.

    One test case is constructed with two volatge sources, where one source is
    between ground(reference node) and node 1 and another voltage source is
    between nodes 2 and 3

    Again attribute will_run is added to this function
    """
    o, d = [1, 3, 1, 2, 3], [2, 2, 0, 0, 0]
    e = ["R1", "V1", "V2", "R2", "R3"]
    (v, v_t, dep) = prog.set_volt_matrix(o, d, e)
    test_output = (Matrix([[0, -1], [1, 0], [-1, 0]]),
                   Matrix([[0, -1, 1], [1, 0, 0]]), Matrix([[0, 0], [0, 0]]))
    assert(v, v_t, dep) == test_output


def test_output_tf_calc():
    """
    Test output of the function output_tf_calc of prog_tf.py.

    This creates the appropriate netlist for a simple series RLC circuit
    with the following parameters.
    V = 10V
    R = 10ohms
    L = 0.01H
    C = 10^-6F
    Nodal analysis of the above circuit is done by hand and provided as sol
    to the function output_tf_calc. Different output parameters such as
    current through inductor, voltage across inductor, voltage across
    capacitor, voltage across voltage source is tested.

    Atrribute will_run is also attached to this test function
    """
    s = symbols('s')
    sol = {}
    impedance = (s**2*1e-8+s*1e-5+1.0)/(s*1e-6)
    iv1, v1, v2 = symbols('I_V1'), symbols('V_1'), symbols('V_2')
    v3 = symbols('V_3')
    sol[iv1] = 10.0/impedance
    sol[v1], sol[v2] = 10.0, 10.0-100.0/impedance
    sol[v3] = 10.0-100.0/impedance-(s*0.1)/impedance
    o, d = [1, 2, 3, 1], [2, 3, 0, 0]
    ident, val = ["R1", "L1", "C1", "V1"], [10, 0.01, 1e-6, 10]
    test_out = prog.output_tf_calc(sol, o, d, val, ident, "L1", "I")
    assert(test_out) == sol[iv1]
    test_out = prog.output_tf_calc(sol, o, d, val, ident, "L1", "V")
    assert(test_out) == sol[iv1]*0.01*s
    test_out = prog.output_tf_calc(sol, o, d, val, ident, "C1", "V")
    assert(test_out) == sol[v3]
    test_out = prog.output_tf_calc(sol, o, d, val, ident, "V1", "V")
    assert(test_out) == 10.0


def test_nodal_matrix():
    """Test the formation of the 3 matrices required for solving nodal analysis.

    A simple series RLC circuit is taken for testing
    """
    s, V_1, V_2 = symbols('s'), symbols('V_1'), symbols('V_2')
    V_3, I_V1 = symbols('V_3'), symbols('I_V1')
    m = Matrix([[0.2, -0.2, 0.0, -1.0], [-0.2, 0.2+0.1/s, -0.1/s, 0.0],
                [0.0, -0.1/s, 0.1/s+1e-6*s, 0.0], [1.0, 0.0, 0.0, 0.0]])
    unknowns = Matrix([[V_1], [V_2], [V_3], [I_V1]])
    rhs = Matrix([[0.0], [0.0], [0.0], [5.0]])
    c = Matrix([[0.2, -0.2, 0.0], [-0.2, 0.2+0.1/s, -0.1/s],
                [0.0, -0.1/s, 0.1/s+1e-6*s]])
    v, v_t = Matrix([[-1.0], [0.0], [0.0]]), Matrix([[1.0, 0.0, 0.0]])
    n_nodes, n_voltsrc, val = 3, 1, [5.0, 10.0, 1e-6, 5.0]
    ele_type, dep = ["R1", "L1", "C1", "V1"], Matrix([[0.0]])
    u, mat, r = prog.nodal_matrix(c, v, val, v_t, n_nodes, n_voltsrc,
                                  ele_type, dep)
    assert(mat, u, r) == (m, unknowns, rhs)


def test_check_netlist_error():
    """Test the function check_netlist_error of prog_tf.py."""
    origin, dest = [1, -2, 3, 1], [2, 3, 0, 0]
    ele_type, val = ['R1', 'L1', 'C1', 'V1'], [10, 0.01, 0.001, 10]
    e_flag, e_msg = prog.check_netlist_error(origin, dest, ele_type, val)
    assert(e_flag, e_msg) == (1, "Negative value of node.")

    origin, dest = [1, 2, 3, 1], [2, 3, 0, 0]
    ele_type, val = ['R1', 'L1', 'C1', 'V1'], [0, 0.01, 0.001, 10]
    e_flag, e_msg = prog.check_netlist_error(origin, dest, ele_type, val)
    assert(e_flag, e_msg) == (1, "Zero value")

    origin, dest = [1, 2, 3, 1], [2, 3, 0, 0]
    ele_type, val = ['R1', 'L1', 'C1', 'V1'], [-10, 0.01, 0.001, 10]
    e_flag, e_msg = prog.check_netlist_error(origin, dest, ele_type, val)
    assert(e_flag, e_msg) == (1, "Non-positive value of R/L/C")

    origin, dest = [1, 2, 3, 1], [2, 3, 0, 0]
    ele_type, val = ['R1', 'L1', 'C1', 'V1'], [10, 0.01, 0.001, 0]
    e_flag, e_msg = prog.check_netlist_error(origin, dest, ele_type, val)
    assert(e_flag, e_msg) == (1, "Zero value")

    origin, dest = [1, 2, 3, 1], [2, 3, 0, 0]
    ele_type, val = ['R1', 'L1', 'V1'], [10, 0.01, 0.001, 10]
    e_flag, e_msg = prog.check_netlist_error(origin, dest, ele_type, val)
    assert(e_flag, e_msg) == (1, "You have not entered all identifiers.")

    origin, dest = [1, 2, 3, 1], [2, 3, 0, 0]
    ele_type, val = ['R1', 'L1', 'C1', 'V1'], [10, 0.01, 0.001, -10]
    e_flag, e_msg = prog.check_netlist_error(origin, dest, ele_type, val)
    assert(e_flag, e_msg) == (0, "")
# Atrribute will_run is added to all the test functions
test_conductance_matrix.will_run = True
test_voltage_matrix.will_run = True
test_output_tf_calc.will_run = True
test_nodal_matrix.will_run = True
test_check_netlist_error.will_run = True
