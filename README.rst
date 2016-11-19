==========================
Circuit Control Parameters
==========================

Circuit Control Parameters is an application that allows one to view different control parameters of an electrical circuit. This has been
developed keeping in mind the problems that arise in actually specifying the circuit to different softwares such as **MATLAB** and even Python's own control module. In most cases (if we are not using **Simulink** in **MATLAB**), we have to compute the transfer function by
hand, and provide this transfer function as coefficients to the software.
In this we hope to bridge this gap by accepting the circuit in the form a standard netlist, by means of a GUI and then provide the same
functionality of Python's Control Module.

Software Requirements
---------------------

- Python 2.7
- numpy 1.3.7
- sympy 1.0
- Tkinter 8.6
- control 0.7.0
- matplotlib 1.5.1