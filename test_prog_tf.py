import pytest
import numpy as np
from sympy import *
from sympy.matrices import *
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
    s=symbols('s')
    m=Matrix.zeros(3,3)
    o,d=[1,0,2,1],[0,2,3,3]
    e,v=["R1","R2","R3","V1"],[0.2,0.2,0.2,5]
    assert(prog.set_cond_matrix(m,o,d,e,v))==Matrix([[5.0,0.0,0.0],[0,10.0,-5.0],[0.0,-5.0,5.0]])
    o,d=[1,2,3,1],[2,3,0,0]
    e,v=["R1","L1","C1","V1"],[5.0,10.0,1e-6,5.0]
    assert(prog.set_cond_matrix(m,o,d,e,v))==Matrix([[0.2,-0.2,0.0],[-0.2,0.2+0.1/s,-0.1/s],[0.0,-0.1/s,0.1/s+1e-06*s]])
    o,d=[1,2,3,3,3,1],[2,3,0,0,0,0]
    e,v=["R1","C1","C2","L1","R2","V1"],[10.0,1e-6,1e-6,10.0,5.0,5.0]
    assert(prog.set_cond_matrix(m,o,d,e,v))==Matrix([[0.1,-0.1,0],[-0.1,0.1+1e-6*s,-1e-6*s],[0,-1e-6*s,s*1e-6+s*1e-6+0.1/s+0.2]])
    m=Matrix.zeros(4,4)
    o,d=[1,2,2,3,3,4,1],[2,3,0,0,4,0,0]
    e,v=["R1","R2","L1","C1","R3","R4","V1"],[10.0,10.0,10.0,1e-6,10.0,10.0,5.0]
    assert(prog.set_cond_matrix(m,o,d,e,v))==Matrix([[0.1,-0.1,0,0],[-0.1,0.2+0.1/s,-0.1,0],[0,-0.1,0.2+1.0e-6*s,-0.1],[0,0,-0.1,0.2]])

def test_voltage_matrix():
    '''
    This tests the formation of the volatge matrix required for nodal analysis.
    One test case is constructed with two volatge sources, where one source is 
    between ground(reference node) and node 1 and another voltage source is between
    nodes 2 and 3

    Again attribute will_run is added to this function
    '''
    m=Matrix.zeros(3,2)
    m_trans=Matrix.zeros(2,3)
    o,d=[1,3,1,2,3],[2,2,0,0,0]
    e=["R1","V1","V2","R2","R3"]
    (v,v_t)=prog.set_volt_matrix(m,m_trans,o,d,e)
    assert(v,v_t)==(Matrix([[0,-1],[1,0],[-1,0]]),Matrix([[0,-1,1],[1,0,0]]))


test_conductance_matrix.will_run=True
test_voltage_matrix.will_run=True
