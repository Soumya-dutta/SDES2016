from sympy import symbols, simplify
from sympy.matrices import Matrix
import prog_tf as prog


def test_conductance_matrix():

    '''
    This tests the formation of the conductance matrix for 4 given networks:
    Network1: Voltage source is not connected to the ground.
    Network2: A simple series RLC circuit
    Network3: A network with three elements connected between two nodes
    Network4: A complex network with 5 nodes (including the reference node)

    In order to test only specific functions we add attributes to the required
    test functions. The attribute used is will_run.

    To run this test use: nosetests -a will_run test_prog_tf.py
    '''
    s = symbols('s')
    m = Matrix.zeros(3, 3)
    o, d = [1, 0, 2, 1], [0, 2, 3, 3]
    e, v = ["R1", "R2", "R3", "V1"], [0.2, 0.2, 0.2, 5]
    test_output = Matrix([[5.0, 0.0, 0.0], [0, 10.0, -5.0], [0.0, -5.0, 5.0]])
    assert(prog.set_cond_matrix(m, o, d, e, v)) == test_output
    o, d = [1, 2, 3, 1], [2, 3, 0, 0]
    e, v = ["R1", "L1", "C1", "V1"], [5.0, 10.0, 1e-6, 5.0]
    test_output = Matrix([[0.2, -0.2, 0.0], [-0.2, 0.2+0.1/s, -0.1/s],
                          [0.0, -0.1/s, 0.1/s+1e-6*s]])
    assert(prog.set_cond_matrix(m, o, d, e, v)) == test_output
    o, d = [1, 2, 3, 3, 3, 1], [2, 3, 0, 0, 0, 0]
    e = ["R1", "C1", "C2", "L1", "R2", "V1"]
    v = [10.0, 1e-6, 1e-6, 10.0, 5.0, 5.0]
    test_output = Matrix([[0.1, -0.1, 0], [-0.1, 0.1+1e-6*s, -1e-6*s],
                          [0, -1e-6*s, 2*s*1e-6+0.1/s+0.2]])
    assert(prog.set_cond_matrix(m, o, d, e, v)) == test_output
    m = Matrix.zeros(4, 4)
    o, d = [1, 2, 2, 3, 3, 4, 1], [2, 3, 0, 0, 4, 0, 0]
    e = ["R1", "R2", "L1", "C1", "R3", "R4", "V1"]
    v = [10.0, 10.0, 10.0, 1e-6, 10.0, 10.0, 5.0]
    test_output = Matrix([[0.1, -0.1, 0, 0], [-0.1, 0.2+0.1/s, -0.1, 0],
                          [0, -0.1, 0.2+1e-6*s, -0.1], [0, 0, -0.1, 0.2]])
    assert(prog.set_cond_matrix(m, o, d, e, v)) == test_output


def test_voltage_matrix():

    '''
    This tests the formation of the volatge matrix required for nodal analysis.
    One test case is constructed with two volatge sources, where one source is
    between ground(reference node) and node 1 and another voltage source is
    between nodes 2 and 3

    Again attribute will_run is added to this function
    '''
    m = Matrix.zeros(3, 2)
    m_trans = Matrix.zeros(2, 3)
    o, d = [1, 3, 1, 2, 3], [2, 2, 0, 0, 0]
    e = ["R1", "V1", "V2", "R2", "R3"]
    (v, v_t) = prog.set_volt_matrix(m, m_trans, o, d, e)
    test_output = (Matrix([[0, -1], [1, 0], [-1, 0]]),
                   Matrix([[0, -1, 1], [1, 0, 0]]))
    assert(v, v_t) == test_output


def test_output_tf_calc():

    '''This is a test for the function output_tf_calc of prog_tf.py.
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
    '''
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
    assert(test_out) == simplify(sol[iv1])
    test_out = prog.output_tf_calc(sol, o, d, val, ident, "L1", "V")
    assert(test_out) == simplify(sol[iv1]*0.01*s)
    test_out = prog.output_tf_calc(sol, o, d, val, ident, "C1", "V")
    assert(test_out) == simplify(sol[v3])
    test_out = prog.output_tf_calc(sol, o, d, val, ident, "V1", "V")
    assert(test_out) == 10.0


test_conductance_matrix.will_run = True
test_voltage_matrix.will_run = True
test_output_tf_calc.will_run = True
